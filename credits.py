import arcade
from menu import MainMenuView

class CreditsView(arcade.View):
    
    def on_show_view(self):
        self.width, self.height = arcade.get_display_size()
        arcade.set_viewport(0, self.width, 0, self.height)
        self.total_time = 0.0
        
        self.music = arcade.load_sound("./Ressources/starting.wav")
        self.music = arcade.play_sound(self.music,volume = 10,looping=False,speed=0.80)
        
        self.About = arcade.Text("Made by CubeLogique", self.window.width / 2, self.window.height / 2, arcade.color.WHITE, font_size=50, anchor_x="center")
        
        self.logo = arcade.load_texture("./Ressources/logo.png")
        self.logo = arcade.Sprite(texture=self.logo,scale=0.25,center_x=self.window.width / 2, center_y=self.window.height / 1.4)
        
        arcade.load_font("./Ressources/joystix.ttf")
        
    def draw_message(self, message, center_x, center_y):
        arcade.draw_text(message, center_x, center_y, arcade.color.WHITE, font_size=40, anchor_x="center", font_name='Joystix')   
        
    def on_draw(self):
        self.clear()
        # arcade.set_background_color(arcade.color.COOL_BLACK)
        arcade.set_background_color(arcade.color.BLACK)
        self.logo.draw()
        if self.seconds >1:
            self.draw_message("Made by JLT",self.window.width / 2, self.window.height / 1.8)
        else:
            pass
        if self.seconds >2:
            self.draw_message("Version 1.0",self.window.width / 2, self.window.height / 5)
        else:
            pass
        if self.seconds >3:
            self.draw_message("Powered by Python",self.window.width / 2, self.window.height / 7)
        else:
            pass
    
    def on_key_press(self, symbol: int, modifiers: int):
        view = MainMenuView()
        arcade.stop_sound(self.music)
        self.window.show_view(view)
            
            
    def on_mouse_press(self, x: int, y: int, button: int, modifiers: int):
        view = MainMenuView()
        arcade.stop_sound(self.music)
        self.window.show_view(view)
        
    def on_update(self, delta_time: float):
        self.total_time += delta_time
        self.seconds = int(self.total_time) % 60
        # if self.seconds>4:
        #     view = MainMenuView()
        #     arcade.stop_sound(self.music)
        #     self.window.show_view(view)
        # else:
        #     pass
        # if self.AboutPosition < 50:
        #     self.About.y =+ 5
        #     self.AboutPosition =+ 1
        # else:
        #     self.AboutPosition = 0
    
    
    # def on_mouse_press(self, x: int, y: int, button: int, modifiers: int):
    #     if super().on_mouse_press(x, y, button, modifiers) == None:
    #         view = MainMenuView()
    #         arcade.stop_sound(self.music)
    #         self.window.show_view(view)
    #     else:
    #         pass