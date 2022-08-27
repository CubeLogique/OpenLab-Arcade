import arcade
import arcade.gui

class KeyboardView(arcade.View):
    
    def on_show_view(self):
        
        self.width, self.height = arcade.get_display_size()
        arcade.set_viewport(0, self.width, 0, self.height)
        arcade.set_background_color(arcade.color.AMAZON)
        
        arcade.load_font("./Ressources/joystix.ttf")
        
        from translator import language
        self.langlist = language.read()
        
        self.manager = arcade.gui.UIManager()
        self.manager.enable()
        self.v_box = arcade.gui.UIBoxLayout()
        
        # settings_text = arcade.gui.UILabel(text="Paramètres",font_size=20,font_name="Arial")
        # self.v_box.add(settings_text.with_space_around(bottom=100))
        
        Logo = arcade.Sprite("./Ressources/logo.png")
        Language = arcade.gui.UILabel(text=self.langlist[5],font_name="Joystix",font_size=20)
        self.v_box.add(Language.with_space_around(bottom=20))
        
        self.manager.add(
            arcade.gui.UIAnchorWidget(
                anchor_x="center",
                anchor_y="top",
                align_y=-100,
                child=self.v_box))
        
        self.keys = []
           
    def on_key_press(self, key, modifiers):
        if len(self.keys) == 0:
            self.clear()
            arcade.draw_text('Gauche', start_x=self.width/2, start_y=self.height/2, color=arcade.color.WHITE, font_size=20, anchor_x="center",font_name="Joystix")
            self.keys.append(key)
        elif len(self.keys) == 1:
            self.clear()
            arcade.draw_text('Haut', start_x=self.width/2, start_y=self.height/2, color=arcade.color.WHITE, font_size=20, anchor_x="center",font_name="Joystix")
            self.keys.append(key)
        elif len(self.keys) == 2:
            self.clear()
            arcade.draw_text('Bas', start_x=self.width/2, start_y=self.height/2, color=arcade.color.WHITE, font_size=20, anchor_x="center",font_name="Joystix")
            self.keys.append(key)
        elif len(self.keys) == 3:
            self.keys.append(key)
            text_file = open("keyboard.txt", "w")
            text_file.write(str(self.keys))
            text_file.close()
            with open("keyboard.txt") as reader:
                keys = reader.read()
                reader.close()
                op = keys.strip('][').split(', ')
                print ("final list", op)
                print (type(op))
            arcade.close_window()
            arcade.exit()
    
    def on_draw(self):
        self.clear()
        self.manager.draw()
        arcade.draw_text("Droite", start_x=self.width/2, start_y=self.height/2, color=arcade.color.WHITE, font_size=20, anchor_x="center",font_name="Joystix")
        
