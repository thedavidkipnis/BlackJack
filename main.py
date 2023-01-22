from screeninfo import get_monitors
import arcade
import arcade.gui
import ButtonStyles as buttonStyles
import GameData as gameData
import BlackJackGame
import UIManager


class SetupMenu(arcade.Window):
    """
    Class that sets up a game of BlackJack. Creates a pop-up window.
    Provides the user with the option to select a number of players,
    or quit the pop-up window.

    screen_width, screen_height = set pop-up window dimensions
    title = sets title for window
    """

    def __init__(self, screen_width, screen_height, title):
        super().__init__(screen_width, screen_height, title)

        self.manager = arcade.gui.UIManager()
        self.manager.enable()

        arcade.set_background_color(arcade.color.GREEN)

        self.v_box = arcade.gui.UIBoxLayout()
        self.h_box = arcade.gui.UIBoxLayout(vertical=False)

        # button disguised as a label
        selection_label = arcade.gui.UIFlatButton(text="Select # of Players", style=buttonStyles.disabled_button,
                                                  width=300, height=100)
        self.v_box.add(selection_label.with_space_around(bottom=20))

        # creating list of buttons for player selection
        for i in range(1, 5):
            selection_button = buttonStyles.PlayerSelectionButton(text=str(i), width=100, height=100, num=i,
                                                     style=buttonStyles.red_style)
            self.h_box.add(selection_button.with_space_around(right=20, left=20))

        self.v_box.add(self.h_box.with_space_around(bottom=100))

        # button for quitting the game
        quit_button = buttonStyles.QuitButton(text="Quit", width=200)
        self.v_box.add(quit_button)

        # adding visual elements to be drawn
        self.manager.add(
            arcade.gui.UIAnchorWidget(
                anchor_x="center_x",
                anchor_y="center_y",
                child=self.v_box)
        )

    # Renders the setup menu
    def on_draw(self):
        self.clear()
        self.manager.draw()


class GameWindow(arcade.Window):
    """
    Main game class. Creates game based on info received from the setup menu. Creates and initializes the card deck,
    players, and all ui elements. Keeps track of main game logic.
    """

    # Method for initializing an instance of main game
    def __init__(self, screen_width, screen_height, title):
        super().__init__(screen_width, screen_height, title)

        self.game = None

        self.ui_manager = None

        self.turn_pointer = None

    # Instantiates game and UI elements list
    def setup(self):
        self.game = BlackJackGame.Game()
        self.game.setup(gameData.NUM_PLAYERS)

        self.ui_manager = UIManager.UIManager(self.game)
        self.ui_manager.setup()

        arcade.set_background_color(arcade.color.GREEN_YELLOW)

    # Draws the lists of sprites - called once per frame
    def on_draw(self):
        self.clear()
        arcade.start_render()

        self.game.card_list.draw()
        self.game.players.draw()
        self.ui_manager.ui_elements.draw()
        self.ui_manager.ui_manager.draw()

    # Updates game elements
    def on_update(self, delta_time: float):
        self.ui_manager.update_pointer()
        self.ui_manager.update_player_action_buttons()


def get_screen_dimensions():
    """
    Fetches screen dimensions from user's device to set game window size

    :return: (int,int)
    """
    screen_width = None
    screen_height = None

    for m in get_monitors():
        if m.is_primary:
            screen_width = m.width
            screen_height = m.height
            return screen_width, screen_height

    return None


def main():
    """
    Sets screen dimensions. Creates SetupMenu and GameWindow instances.
    """
    screen_dimensions = get_screen_dimensions()

    if screen_dimensions is None:
        print("Error fetching screen dimensions.")
        return

    gameData.SCREEN_X = screen_dimensions[0]
    gameData.SCREEN_Y = screen_dimensions[1]

    setup_window = SetupMenu(600, 800, "Black Jack Setup")
    setup_window.run()

    if gameData.NUM_PLAYERS is None:
        arcade.exit()
        return

    game_window = GameWindow(gameData.SCREEN_X,
                             gameData.SCREEN_Y,
                             "Black Jack")
    game_window.setup()
    game_window.run()


if __name__ == "__main__":
    main()
