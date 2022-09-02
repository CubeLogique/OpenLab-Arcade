import arcade
import arcade.gui

class SettingsView(arcade.View):
    
    def on_show_view(self):
        
        self.width, self.height = arcade.get_display_size()
        print("Screen Size is",self.width,self.height)
        # arcade.set_viewport(0, self.width, 0, self.height)
        
        arcade.load_font("./Ressources/joystix.ttf")
        
        from translator import language
        self.langlist = language.read()
        
        self.manager = arcade.gui.UIManager()
        self.manager.enable()
        ui_anchor_layout = arcade.gui.UIAnchorLayout()
        self.v_box = arcade.gui.UIBoxLayout()
        
        # settings_text = arcade.gui.UILabel(text="Paramètres",font_size=20,font_name="Arial")
        # self.v_box.add(settings_text.with_space_around(bottom=100))
        
        Language = arcade.gui.UILabel(text="Language",font_name='Joystix Monospace',font_size=20)
        self.v_box.add(Language)
        
        French_button = arcade.gui.UIFlatButton(text="Français", width=200)
        self.v_box.add(French_button.with_padding(top=10,bottom=10))
        
        French_button.on_click = self.on_click_french
        
        English_button = arcade.gui.UIFlatButton(text="English", width=200)
        self.v_box.add(English_button.with_padding(bottom=20))
        
        English_button.on_click = self.on_click_english
    
        Keyboard = arcade.gui.UILabel(text=self.langlist[4],font_name='Joystix Monospace',font_size=20)
        self.v_box.add(Keyboard)
        
               
        ui_text_label = arcade.gui.UITextArea(text=self.langlist[7],
                                              width=400,
                                              height=60,
                                              font_size=12)
        
        self.v_box.add(ui_text_label.with_padding(top=20))
        
        # self.manager.add(
        #     arcade.gui.UIAnchorWidget(
        #         anchor_x="center",
        #         align_x=100,
        #         anchor_y="center_y",
        #         align_y=-50,
        #         child=self.v_box))
        
        ui_anchor_layout.add(child=self.v_box, anchor_x="right", anchor_y="center_y",align_x=-100,align_y=-150)
        self.manager.add(ui_anchor_layout)
        
        self.logo = arcade.Sprite("./Ressources/logo.png",scale=0.40,center_x=self.v_box.center_x + self.width/1.4,center_y=self.v_box.center_y + self.height/1.3)
        
    def on_click_french(self, event):
        text_file = open("language.txt", "w")
        text_file.write('Français')
        text_file.close()
        with open("language.txt") as reader:
            Language_Selected = reader.read()
        from menu import MainMenuView
        view = MainMenuView()
        self.window.show_view(view)
        
    def on_click_english(self, event):
        text_file = open("language.txt", "w")
        text_file.write('English')
        text_file.close()
        with open("language.txt") as reader:
            Language_Selected = reader.read()
            reader.close()
        from menu import MainMenuView
        view = MainMenuView()
        self.window.show_view(view)
        
    def on_click_keyboard(self,event):
        from keyboard import KeyboardView
        view = KeyboardView()
        self.window.show_view(view)
    
    def on_draw(self):
        self.clear()
        arcade.draw_lrwh_rectangle_textured(0, 0,
                                            self.width, self.height,
                                            arcade.load_texture("./Ressources/background.png"))
        arcade.draw_text(self.langlist[1], start_x=self.logo.center_x, start_y=self.logo.center_y-self.height/6.2, color=arcade.color.WHITE, font_size=30, anchor_x="left",font_name='Joystix Monospace')
        self.logo.draw()
        self.manager.draw()