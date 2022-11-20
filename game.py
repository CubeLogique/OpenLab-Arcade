import arcade
import pymunk

SCREEN_TITLE = "Prototype"

# Size of screen to show, in pixels
SCREEN_WIDTH = 800
SCREEN_HEIGHT = 600


class GameWindow(arcade.Window):

    def __init__(self, width, height, title):
        super().__init__(width, height, title)

    def setup(self):
        pass

    def on_key_press(self, key, modifiers):
        pass

    def on_key_release(self, key, modifiers):
        pass

    def on_update(self, delta_time):
        pass

    def on_draw(self):
        self.clear()


def main():
    window = GameWindow(SCREEN_WIDTH, SCREEN_HEIGHT, SCREEN_TITLE)
    window.setup()
    arcade.run()


if __name__ == "__main__":
    main()