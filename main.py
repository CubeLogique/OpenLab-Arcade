import arcade
import arcade.gui
from pyglet.app import run

SCREEN_TITLE = "OpenLab"
# SCREEN_GRID_WIDTH = SCREEN_WIDTH / SPRITE_SIZE
# SCREEN_GRID_HEIGHT = SCREEN_HEIGHT / SPRITE_SIZE

# Fonction Principale
def main():
    from menu import MainMenuView
    window = arcade.Window(title=SCREEN_TITLE, fullscreen=True)
    start_view = MainMenuView()
    window.show_view(start_view)
    run(1/120)

# Point de Démarrage
if __name__ == "__main__":
    main()