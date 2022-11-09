import arcade
import arcade.gui
import math
from typing import Optional

GRAVITY = 1500
DEFAULT_DAMPING = 1.0
PLAYER_DAMPING = 0.4
PLAYER_FRICTION = 1.0
WALL_FRICTION = 0.7
DYNAMIC_ITEM_FRICTION = 0.6
PLAYER_MASS = 2.0
PLAYER_MAX_HORIZONTAL_SPEED = 450
PLAYER_MAX_VERTICAL_SPEED = 1600
PLAYER_MOVE_FORCE_ON_GROUND = 8000
PLAYER_MOVE_FORCE_IN_AIR = 900
PLAYER_JUMP_IMPULSE = 1800
DEAD_ZONE = 0.1
RIGHT_FACING = 0
LEFT_FACING = 1
DISTANCE_TO_CHANGE_TEXTURE = 20
BULLET_MOVE_FORCE = 4500
BULLET_MASS = 0.1
BULLET_GRAVITY = 0
UPDATES_PER_FRAME = 5
SPRITE_SCALING = 0.5
VIEWPORT_MARGIN = 40
MOVEMENT_SPEED = 5
IMAGE_ROTATION = 90

SPRITE_IMAGE_SIZE = 128
SPRITE_SCALING_PLAYER = 0.5
SPRITE_SCALING_TILES = 0.5
SPRITE_SIZE = int(SPRITE_IMAGE_SIZE * SPRITE_SCALING_PLAYER)

SCREEN_GRID_WIDTH = 16
SCREEN_GRID_HEIGHT = 10
# SCREEN_WIDTH = SPRITE_SIZE * SCREEN_GRID_WIDTH
# SCREEN_HEIGHT = SPRITE_SIZE * SCREEN_GRID_HEIGHT

TILE_SCALING = SCREEN_GRID_HEIGHT / SCREEN_GRID_WIDTH

class PlayerSprite(arcade.Sprite):
    
    def __init__(self,
                 ladder_list: arcade.SpriteList,
                 hit_box_algorithm):
        
        super().__init__()
        self.scale = SPRITE_SCALING_PLAYER

        main_path = ":resources:images/animated_characters/female_person/femalePerson"

        # Load textures for idle standing
        self.idle_texture_pair = arcade.load_texture_pair(f"{main_path}_idle.png",
                                                          hit_box_algorithm=hit_box_algorithm)
        self.jump_texture_pair = arcade.load_texture_pair(f"{main_path}_jump.png")
        self.fall_texture_pair = arcade.load_texture_pair(f"{main_path}_fall.png")

        # Load textures for walking
        self.walk_textures = []
        for i in range(8):
            texture = arcade.load_texture_pair(f"{main_path}_walk{i}.png")
            self.walk_textures.append(texture)

        # Load textures for climbing
        self.climbing_textures = []
        texture = arcade.load_texture(f"{main_path}_climb0.png")
        self.climbing_textures.append(texture)
        texture = arcade.load_texture(f"{main_path}_climb1.png")
        self.climbing_textures.append(texture)

        # Set the initial texture
        self.texture = self.idle_texture_pair[0]

        # Hit box will be set based on the first image used.
        self.hit_box = self.texture.hit_box_points

        # Default to face-right
        self.character_face_direction = RIGHT_FACING

        # Index of our current texture
        self.cur_texture = 0

        # How far have we traveled horizontally since changing the texture
        self.x_odometer = 0
        self.y_odometer = 0

        self.ladder_list = ladder_list
        self.is_on_ladder = False

    def pymunk_moved(self, physics_engine, dx, dy, d_angle):
        # Figure out if we need to face left or right
        if dx < -DEAD_ZONE and self.character_face_direction == RIGHT_FACING:
            self.character_face_direction = LEFT_FACING
        elif dx > DEAD_ZONE and self.character_face_direction == LEFT_FACING:
            self.character_face_direction = RIGHT_FACING

        # Are we on the ground?
        is_on_ground = physics_engine.is_on_ground(self)

        # Are we on a ladder?
        if len(arcade.check_for_collision_with_list(self, self.ladder_list)) > 0:
            if not self.is_on_ladder:
                self.is_on_ladder = True
                self.pymunk.gravity = (0, 0)
                self.pymunk.damping = 0.0001
                self.pymunk.max_vertical_velocity = PLAYER_MAX_HORIZONTAL_SPEED
        else:
            if self.is_on_ladder:
                self.pymunk.damping = 1.0
                self.pymunk.max_vertical_velocity = PLAYER_MAX_VERTICAL_SPEED
                self.is_on_ladder = False
                self.pymunk.gravity = None

        # Add to the odometer how far we've moved
        self.x_odometer += dx
        self.y_odometer += dy

        if self.is_on_ladder and not is_on_ground:
            # Have we moved far enough to change the texture?
            if abs(self.y_odometer) > DISTANCE_TO_CHANGE_TEXTURE:

                # Reset the odometer
                self.y_odometer = 0

                # Advance the walking animation
                self.cur_texture += 1

            if self.cur_texture > 1:
                self.cur_texture = 0
            self.texture = self.climbing_textures[self.cur_texture]
            return

        # Jumping animation
        if not is_on_ground:
            if dy > DEAD_ZONE:
                self.texture = self.jump_texture_pair[self.character_face_direction]
                return
            elif dy < -DEAD_ZONE:
                self.texture = self.fall_texture_pair[self.character_face_direction]
                return

        # Idle animation
        if abs(dx) <= DEAD_ZONE:
            self.texture = self.idle_texture_pair[self.character_face_direction]
            return

        # Have we moved far enough to change the texture?
        if abs(self.x_odometer) > DISTANCE_TO_CHANGE_TEXTURE:

            # Reset the odometer
            self.x_odometer = 0

            # Advance the walking animation
            self.cur_texture += 1
            if self.cur_texture > 7:
                self.cur_texture = 0
            self.texture = self.walk_textures[self.cur_texture][self.character_face_direction]
            
# class BulletSprite(arcade.SpriteSolidColor):
#     def pymunk_moved(self, physics_engine, dx, dy, d_angle):
#         # If the bullet falls below the screen, remove it
#         if self.center_y < -100:
#             self.remove_from_sprite_lists()

class GravityBall(arcade.Sprite):
    def __init__(self):
        super().__init__(":resources:images/topdown_tanks/tank_green.png")

        self._destination_point = None
        self.speed = 10
        self.rot_speed = 5

    @property
    def destination_point(self):
        return self._destination_point

    @destination_point.setter
    def destination_point(self, destination_point):
        self._destination_point = destination_point

    def on_update(self, delta_time: float = 1 / 60):
        
        if not self._destination_point:
            self.change_x = 0
            self.change_y = 0
            return

        start_x = self.center_x
        start_y = self.center_y

        dest_x = self._destination_point[0]
        dest_y = self._destination_point[1]

        x_diff = dest_x - start_x
        y_diff = dest_y - start_y
        target_angle_radians = math.atan2(y_diff, x_diff)
        if target_angle_radians < 0:
            target_angle_radians += 2 * math.pi

        actual_angle_radians = math.radians(self.angle - IMAGE_ROTATION)
        rot_speed_radians = math.radians(self.rot_speed)
        angle_diff_radians = target_angle_radians - actual_angle_radians

        if abs(angle_diff_radians) <= rot_speed_radians:
            actual_angle_radians = target_angle_radians
            clockwise = None
        elif angle_diff_radians > 0 and abs(angle_diff_radians) < math.pi:
            clockwise = False
        elif angle_diff_radians > 0 and abs(angle_diff_radians) >= math.pi:
            clockwise = True
        elif angle_diff_radians < 0 and abs(angle_diff_radians) < math.pi:
            clockwise = True
        else:
            clockwise = False

        # Rotate the proper direction if needed
        if actual_angle_radians != target_angle_radians and clockwise:
            actual_angle_radians -= rot_speed_radians
        elif actual_angle_radians != target_angle_radians:
            actual_angle_radians += rot_speed_radians

        # Keep in a range of 0 to 2pi
        if actual_angle_radians > 2 * math.pi:
            actual_angle_radians -= 2 * math.pi
        elif actual_angle_radians < 0:
            actual_angle_radians += 2 * math.pi

        # Convert back to degrees
        self.angle = math.degrees(actual_angle_radians) + IMAGE_ROTATION

        # Are we close to the correct angle? If so, move forward.
        if abs(angle_diff_radians) < math.pi / 4:
            self.change_x = math.cos(actual_angle_radians) * self.speed
            self.change_y = math.sin(actual_angle_radians) * self.speed

        # Fine-tune our change_x/change_y if we are really close to destination
        # point and just need to set to that location.
        traveling = False
        if abs(self.center_x - dest_x) < abs(self.change_x):
            self.center_x = dest_x
        else:
            self.center_x += self.change_x
            traveling = True

        if abs(self.center_y - dest_y) < abs(self.change_y):
            self.center_y = dest_y
        else:
            self.center_y += self.change_y
            traveling = True

        # If we have arrived, then cancel our destination point
        if not traveling:
            self._destination_point = None

class GameplayView(arcade.View):
    
    def __init__(self):
        
        super().__init__()
        
        self.width, self.height = arcade.get_display_size()
        arcade.set_viewport(0, self.width, 0, self.height)
        
        self.camera = arcade.Camera(viewport_width=self.width, viewport_height=self.height)
        self.camera.use()

    def on_show_view(self):
        
        SPRITE_SIZE = self.height / SCREEN_GRID_HEIGHT

        # Player sprite
        self.player_sprite: Optional[PlayerSprite] = None

        # Sprite lists we need
        self.player_list: Optional[arcade.SpriteList] = None
        self.wall_list: Optional[arcade.SpriteList] = None
        self.bullet_list: Optional[arcade.SpriteList] = None
        self.item_list: Optional[arcade.SpriteList] = None
        self.moving_sprites_list: Optional[arcade.SpriteList] = None
        self.ladder_list: Optional[arcade.SpriteList] = None

        # Track the current state of what key is pressed
        self.left_pressed: bool = False
        self.right_pressed: bool = False
        self.up_pressed: bool = False
        self.down_pressed: bool = False

        # Physics engine
        self.physics_engine: Optional[arcade.PymunkPhysicsEngine] = None

        # Set background color
        arcade.set_background_color(arcade.color.AMAZON)

        # Create the sprite lists
        self.player_list = arcade.SpriteList()
        # self.bullet_list = arcade.SpriteList()

        # Map name
        map_name = ":resources:/tiled_maps/pymunk_test_map.json"

        # Load in TileMap
        tile_map = arcade.load_tilemap(map_name, SPRITE_SCALING_TILES)

        # Pull the sprite layers out of the tile map
        self.wall_list = tile_map.sprite_lists["Platforms"]
        self.item_list = tile_map.sprite_lists["Dynamic Items"]
        self.ladder_list = tile_map.sprite_lists["Ladders"]
        self.moving_sprites_list = tile_map.sprite_lists['Moving Platforms']

        # Create player sprite
        self.player_sprite = PlayerSprite(self.ladder_list, hit_box_algorithm="Detailed")

        # Set player location
        grid_x = 1
        grid_y = 1
        self.player_sprite.center_x = SPRITE_SIZE * grid_x + SPRITE_SIZE / 2
        self.player_sprite.center_y = SPRITE_SIZE * grid_y + SPRITE_SIZE / 2
        # Add to player sprite list
        self.player_list.append(self.player_sprite)

        # --- Pymunk Physics Engine Setup ---

        # The default damping for every object controls the percent of velocity
        # the object will keep each second. A value of 1.0 is no speed loss,
        # 0.9 is 10% per second, 0.1 is 90% per second.
        # For top-down games, this is basically the friction for moving objects.
        # For platformers with gravity, this should probably be set to 1.0.
        # Default value is 1.0 if not specified.
        damping = DEFAULT_DAMPING

        # Set the gravity. (0, 0) is good for outer space and top-down.
        self.gravity = (0, -GRAVITY)

        # Create the physics engine
        self.physics_engine = arcade.PymunkPhysicsEngine(damping=damping,
                                                         gravity=self.gravity)
        
        

        def wall_hit_handler(bullet_sprite, _wall_sprite, _arbiter, _space, _data):
            bullet_sprite.remove_from_sprite_lists()

        self.physics_engine.add_collision_handler("bullet", "wall", post_handler=wall_hit_handler)

        def item_hit_handler(bullet_sprite, item_sprite, _arbiter, _space, _data):
            bullet_sprite.remove_from_sprite_lists()
            item_sprite.remove_from_sprite_lists()

        self.physics_engine.add_collision_handler("bullet", "item", post_handler=item_hit_handler)

        # Add the player.
        # For the player, we set the damping to a lower value, which increases
        # the damping rate. This prevents the character from traveling too far
        # after the player lets off the movement keys.
        # Setting the moment to PymunkPhysicsEngine.MOMENT_INF prevents it from
        # rotating.
        # Friction normally goes between 0 (no friction) and 1.0 (high friction)
        # Friction is between two objects in contact. It is important to remember
        # in top-down games that friction moving along the 'floor' is controlled
        # by damping.
        self.physics_engine.add_sprite(self.player_sprite,
                                       friction=PLAYER_FRICTION,
                                       mass=PLAYER_MASS,
                                       moment_of_inertia=arcade.PymunkPhysicsEngine.MOMENT_INF,
                                       collision_type="player",
                                       max_horizontal_velocity=PLAYER_MAX_HORIZONTAL_SPEED,
                                       max_vertical_velocity=PLAYER_MAX_VERTICAL_SPEED)

        # Create the walls.
        # By setting the body type to PymunkPhysicsEngine.STATIC the walls can't
        # move.
        # Movable objects that respond to forces are PymunkPhysicsEngine.DYNAMIC
        # PymunkPhysicsEngine.KINEMATIC objects will move, but are assumed to be
        # repositioned by code and don't respond to physics forces.
        # Dynamic is default.
        self.physics_engine.add_sprite_list(self.wall_list,
                                            friction=WALL_FRICTION,
                                            collision_type="wall",
                                            body_type=arcade.PymunkPhysicsEngine.STATIC)

        # Create the items
        self.physics_engine.add_sprite_list(self.item_list,
                                            friction=DYNAMIC_ITEM_FRICTION,
                                            collision_type="item")

        # Add kinematic sprites
        self.physics_engine.add_sprite_list(self.moving_sprites_list,
                                            body_type=arcade.PymunkPhysicsEngine.KINEMATIC)

    def center_camera_to_player(self):
 
        screen_center_x = self.player_sprite.center_x - (self.camera.viewport_width / 2)
        screen_center_y = self.player_sprite.center_y - (self.camera.viewport_height / 2)

        # # Don't let camera travel past 0
        # if screen_center_x < 0:
        #     screen_center_x = 0
        # if screen_center_y < 0:
        #     screen_center_y = 0
        player_centered = screen_center_x, screen_center_y

        self.camera.move_to(player_centered)

    def on_key_press(self, key, modifiers):

        if key == arcade.key.LEFT:
            self.left_pressed = True
        elif key == arcade.key.RIGHT:
            self.right_pressed = True
        elif key == arcade.key.UP:
            self.up_pressed = True
            if self.physics_engine.is_on_ground(self.player_sprite) \
                    and not self.player_sprite.is_on_ladder:
                impulse = (0, PLAYER_JUMP_IMPULSE)
                self.physics_engine.apply_impulse(self.player_sprite, impulse)
        elif key == arcade.key.DOWN:
            self.down_pressed = True

    def on_key_release(self, key, modifiers):

        if key == arcade.key.LEFT:
            self.left_pressed = False
        elif key == arcade.key.RIGHT:
            self.right_pressed = False
        elif key == arcade.key.UP:
            self.up_pressed = False
        elif key == arcade.key.DOWN:
            self.down_pressed = False

    def on_mouse_press(self, x, y, button, modifiers):

        # bullet = BulletSprite(20, 5, arcade.color.DARK_YELLOW)
        # self.bullet_list.append(bullet)

        # start_x = self.player_sprite.center_x
        # start_y = self.player_sprite.center_y
        # bullet.position = self.player_sprite.position
        
        # dest_x = x
        # dest_y = y

        # x_diff = dest_x - start_x
        # y_diff = dest_y - start_y
        # angle = math.atan2(y_diff, x_diff)

        # size = max(self.player_sprite.width, self.player_sprite.height) / 2

        # bullet.center_x += size * math.cos(angle)
        # bullet.center_y += size * math.sin(angle)

        # bullet.angle = math.degrees(angle)
        
        # bullet_gravity = (0, -BULLET_GRAVITY)

        # # Add the sprite. This needs to be done AFTER setting the fields above.
        # self.physics_engine.add_sprite(bullet,
        #                                mass=BULLET_MASS,
        #                                damping=1.0,
        #                                friction=0.6,
        #                                collision_type="bullet",
        #                                gravity=bullet_gravity,
        #                                elasticity=0.9)

        # # Add force to bullet
        # force = (BULLET_MOVE_FORCE, 0)
        # self.physics_engine.apply_force(bullet, force)
        
        if button == arcade.MOUSE_BUTTON_RIGHT:
            self.ball.destination_point = x, y
    
    
    def gravity_switch(self,orientation):
        if orientation == "up":
            self.camera.rotation = 180
            self.player_sprite.angle = 180
            self.gravity = (0,GRAVITY)
        elif orientation == "left":
            self.camera.rotation = 90
            self.player_sprite.angle = 90
            self.gravity = (-GRAVITY,0)
        elif orientation == "right":
            self.camera.rotation = 270
            self.player_sprite.angle = 270
            self.gravity = (GRAVITY,0)
        else:
            self.camera.rotation = 0
            self.player_sprite.angle = 0

    def on_update(self, delta_time):
        
        self.center_camera_to_player()
        
        self.ball = GravityBall()
        self.ball.center_x = self.player_sprite.center_x
        self.ball.center_y = self.player_sprite.center_y
        self.player_list.append(self.ball)
        
        self.player_list.on_update(delta_time) 
        
        is_on_ground = self.physics_engine.is_on_ground(self.player_sprite)
        # Update player forces based on keys pressed
        if self.left_pressed and not self.right_pressed:
            # Create a force to the left. Apply it.
            if is_on_ground or self.player_sprite.is_on_ladder:
                force = (-PLAYER_MOVE_FORCE_ON_GROUND, 0)
            else:
                force = (-PLAYER_MOVE_FORCE_IN_AIR, 0)
            self.physics_engine.apply_force(self.player_sprite, force)
            # Set friction to zero for the player while moving
            self.physics_engine.set_friction(self.player_sprite, 0)
        elif self.right_pressed and not self.left_pressed:
            # Create a force to the right. Apply it.
            if is_on_ground or self.player_sprite.is_on_ladder:
                force = (PLAYER_MOVE_FORCE_ON_GROUND, 0)
            else:
                force = (PLAYER_MOVE_FORCE_IN_AIR, 0)
            self.physics_engine.apply_force(self.player_sprite, force)
            # Set friction to zero for the player while moving
            self.physics_engine.set_friction(self.player_sprite, 0)
        elif self.up_pressed and not self.down_pressed:
            # Create a force to the right. Apply it.
            if self.player_sprite.is_on_ladder:
                force = (0, PLAYER_MOVE_FORCE_ON_GROUND)
                self.physics_engine.apply_force(self.player_sprite, force)
                # Set friction to zero for the player while moving
                self.physics_engine.set_friction(self.player_sprite, 0)
        elif self.down_pressed and not self.up_pressed:
            # Create a force to the right. Apply it.
            if self.player_sprite.is_on_ladder:
                force = (0, -PLAYER_MOVE_FORCE_ON_GROUND)
                self.physics_engine.apply_force(self.player_sprite, force)
                # Set friction to zero for the player while moving
                self.physics_engine.set_friction(self.player_sprite, 0)

        else:
            # Player's feet are not moving. Therefore up the friction so we stop.
            self.physics_engine.set_friction(self.player_sprite, 1.0)

        # Move items in the physics engine
        self.physics_engine.step()

        # For each moving sprite, see if we've reached a boundary and need to
        # reverse course.
        for moving_sprite in self.moving_sprites_list:
            if moving_sprite.boundary_right and \
                    moving_sprite.change_x > 0 and \
                    moving_sprite.right > moving_sprite.boundary_right:
                moving_sprite.change_x *= -1
            elif moving_sprite.boundary_left and \
                    moving_sprite.change_x < 0 and \
                    moving_sprite.left > moving_sprite.boundary_left:
                moving_sprite.change_x *= -1
            if moving_sprite.boundary_top and \
                    moving_sprite.change_y > 0 and \
                    moving_sprite.top > moving_sprite.boundary_top:
                moving_sprite.change_y *= -1
            elif moving_sprite.boundary_bottom and \
                    moving_sprite.change_y < 0 and \
                    moving_sprite.bottom < moving_sprite.boundary_bottom:
                moving_sprite.change_y *= -1

            # Figure out and set our moving platform velocity.
            # Pymunk uses velocity is in pixels per second. If we instead have
            # pixels per frame, we need to convert.
            velocity = (moving_sprite.change_x * 1 / delta_time, moving_sprite.change_y * 1 / delta_time)
            self.physics_engine.set_velocity(moving_sprite, velocity)   

    def on_draw(self):
        self.clear()
        self.camera.use()
        self.wall_list.draw()
        self.ladder_list.draw()
        self.moving_sprites_list.draw()
        # self.bullet_list.draw()
        self.item_list.draw()
        self.player_list.draw()