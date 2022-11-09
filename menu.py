import arcade
import arcade.gui
import os
import random

class RotatingSprite(arcade.Sprite):

    def rotate_around_point(self, point, degrees, change_angle=True):

        if change_angle:
            self.angle += degrees

        self.position = arcade.rotate_point(
            self.center_x, self.center_y,
            point[0], point[1], degrees)

class MainMenuView(arcade.View):

    def __init__(self):

        self.sprites = arcade.SpriteList()

        super().__init__()
        
        self.frame_earth = 0
        self.frame_moon = 0
        self.earth_frames = [arcade.load_texture(f"./Ressources/earth_sprites/earth-{i}.png", hit_box_algorithm=None) for i in range(100)]
        self.moon_frames = [arcade.load_texture(f"./Ressources/moon_sprites/moon-{i}.png", hit_box_algorithm=None) for i in range(120)]
        
        from config import read_saved_language, read_language
        
        arcade.load_font("./Ressources/joystix.ttf")

        self.manager = arcade.gui.UIManager()
        self.manager.enable()
        ui_anchor_layout = arcade.gui.UIAnchorLayout()
        self.v_box = arcade.gui.UIBoxLayout()

        print(read_language(read_saved_language(),1))
        start_button = arcade.gui.UIFlatButton(text=read_language(read_saved_language(),0), width=200)
        self.v_box.add(start_button.with_padding(bottom=20))

        start_button.on_click = self.on_click_start
        
        settings_button = arcade.gui.UIFlatButton(text=read_language(read_saved_language(),1), width=200)
        self.v_box.add(settings_button.with_padding(bottom=20))
        
        settings_button.on_click = self.on_click_settings
        
        exit_button = start_button = arcade.gui.UIFlatButton(text=read_language(read_saved_language(),3), width=200)
        self.v_box.add(exit_button.with_padding(bottom=20))
        
        exit_button.on_click = self.on_click_exit

        ui_anchor_layout.add(child=self.v_box, anchor_x="left", anchor_y="center_y",align_x=100,align_y=-50)
        self.manager.add(ui_anchor_layout)
        
        # Réglages Fenêtre
        file_path = os.path.dirname(os.path.abspath(__file__))
        os.chdir(file_path)
        self.width, self.height = arcade.get_display_size()
        print("Screen Size is",self.width,self.height)
        arcade.set_viewport(0, self.width, 0, self.height)
        
        QUARTER_WIDTH = self.width // 4
        HALF_HEIGHT = self.height // 2

        self.moon = RotatingSprite(texture=self.moon_frames[0], scale=1, center_x=2 * QUARTER_WIDTH + 50, center_y=HALF_HEIGHT)

        self.earth = arcade.Sprite(texture=self.earth_frames[0], scale=2.5, center_x=self.width, center_y=0)
        
        self.sprites.extend([self.earth, self.moon])
        
        self.music = self.music = arcade.load_sound("./Ressources/credits.wav")
        speed_list = [0.75,0.80]
        self.music = arcade.play_sound(self.music,volume = 0.2,looping=True,speed=random.choice(speed_list))
        
        self.logo = arcade.Sprite("./Ressources/logo.png",scale=0.40,center_x=self.v_box.center_x + self.width/3.5,center_y=self.v_box.center_y + self.height/1.4)
        
    def on_update(self, delta_time: float):
        self.moon.rotate_around_point(self.earth.position, 60 * delta_time, False)
        # print(self.planet_textures[0])
        if self.frame_earth < 100:
            self.earth.texture = self.earth_frames[self.frame_earth]
            self.frame_earth = self.frame_earth + 1
        else:
            self.frame_earth = 0
        if self.frame_moon < 120:
            self.moon.texture = self.moon_frames[self.frame_moon]
            self.frame_moon =+ self.frame_moon + 1
        else:
            self.frame_moon = 0

    def on_draw(self):
        
        self.clear()
        arcade.draw_lrwh_rectangle_textured(0, 0,
                                            self.width, self.height,
                                            arcade.load_texture("./Ressources/background.png"))
        self.sprites.draw(pixelated=True)
        
        left, screen_width, bottom, screen_height = arcade.get_viewport()
            
        self.manager.draw()
        self.earth.center_x=self.width
        self.logo.draw()
       
    def on_click_start(self, event):
        from Ressources.old.game import GameplayView
        game_view = GameplayView()
        arcade.stop_sound(self.music)
        self.window.show_view(game_view)
    
    def on_click_settings(self, event):
        from settings import SettingsView
        view = SettingsView()
        arcade.stop_sound(self.music)
        self.window.show_view(view)
    
    def on_click_exit(self, event):
        arcade.close_window()
        arcade.exit()
