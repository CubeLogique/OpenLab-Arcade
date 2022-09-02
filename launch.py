import arcade
from menu import MainMenuView

class LaunchView(arcade.View):
    
    def on_show_view(self):
        self.width, self.height = arcade.get_display_size()
        arcade.set_viewport(0, self.width, 0, self.height)
        self.total_time = 0.0
        
    def on_draw(self):
        self.clear()
        arcade.set_background_color(arcade.color.BLACK)
        arcade.load_font("./Ressources/joystix.ttf")
        arcade.draw_text("Made by CubeLogique", self.window.width / 2, self.window.height / 2, arcade.color.WHITE, font_size=40, anchor_x="center", font_name='Joystix Monospace')
        
    def on_update(self, delta_time: float):
        self.total_time += delta_time
        self.seconds = int(self.total_time) % 60
        if self.seconds>1:
            view = MainMenuView()
            self.window.show_view(view)
        else:
            pass