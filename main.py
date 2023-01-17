from screeninfo import get_monitors
import os
import random
import arcade
import arcade.gui
import ButtonStyles as buttonStyles
import GameData as gameData
import Card
import Player


class TestButton(arcade.gui.UIFlatButton):
    def on_click(self, event: arcade.gui.UIOnClickEvent):
        gameData.CURRENT_TURN = (gameData.CURRENT_TURN + 1) % gameData.NUM_PLAYERS


class QuitButton(arcade.gui.UIFlatButton):
    def on_click(self, event: arcade.gui.UIOnClickEvent):
        arcade.exit()


class PlayerSelectionButton(arcade.gui.UIFlatButton):
    def __init__(self,
                 x: float = 0,
                 y: float = 0,
                 width: float = 100,
                 height: float = 50,
                 text="",
                 size_hint=None,
                 size_hint_min=None,
                 size_hint_max=None,
                 style=None,
                 num=None,
                 **kwargs):
        super().__init__(x, y, width, height, text, size_hint, size_hint_min, size_hint_max, style)
        self.num = num

    def on_click(self, event: arcade.gui.UIOnClickEvent):
        gameData.NUM_PLAYERS = self.num
        arcade.close_window()


class SetupMenu(arcade.Window):
    def __init__(self, screen_width, screen_height, title):
        super().__init__(screen_width, screen_height, title)

        self.manager = arcade.gui.UIManager()
        self.manager.enable()

        arcade.set_background_color(arcade.color.GREEN)

        self.v_box = arcade.gui.UIBoxLayout()
        self.h_box = arcade.gui.UIBoxLayout(vertical=False)

        selection_label = arcade.gui.UIFlatButton(text="Select # of Players", style=buttonStyles.disabled_button,
                                                  width=300, height=100)
        self.v_box.add(selection_label.with_space_around(bottom=20))

        for i in range(1, 5):
            selection_button = PlayerSelectionButton(text=str(i), width=100, height=100, num=i,
                                                     style=buttonStyles.red_style)
            self.h_box.add(selection_button.with_space_around(right=20, left=20))

        self.v_box.add(self.h_box.with_space_around(bottom=100))

        quit_button = QuitButton(text="Quit", width=200)
        self.v_box.add(quit_button)

        self.manager.add(
            arcade.gui.UIAnchorWidget(
                anchor_x="center_x",
                anchor_y="center_y",
                child=self.v_box)
        )

    # Draws the setup menu
    def on_draw(self):
        self.clear()
        self.manager.draw()


class GameWindow(arcade.Window):
    def __init__(self, screen_width, screen_height, player_count, title):
        super().__init__(screen_width, screen_height, title)

        self.manager = arcade.gui.UIManager()
        self.manager.enable()

        self.player_count = player_count

        self.players = None
        self.card_list = None
        self.ui_elements = None

        self.turn_pointer = None

        arcade.set_background_color(arcade.color.GREEN_YELLOW)

    def setup(self):
        self.players = generate_players(self.player_count)
        self.card_list = generate_card_deck()
        self.ui_elements = arcade.SpriteList()

        gameData.CURRENT_TURN = 0

        self.turn_pointer = arcade.Sprite("UI_Sprites/Pointer.png",
                                     gameData.UI_SPRITE_SCALING,
                                     center_x=self.players[0].center_x,
                                     center_y=self.players[0].center_y - self.players[0].height)

        self.ui_elements.append(self.turn_pointer)

    def on_draw(self):
        self.clear()
        arcade.start_render()

        self.manager.draw()
        self.card_list.draw()
        self.players.draw()
        self.ui_elements.draw()

    def on_update(self, delta_time: float):
        self.turn_pointer.center_x = self.players[gameData.CURRENT_TURN].center_x
        self.turn_pointer.center_y = self.players[gameData.CURRENT_TURN].center_y - self.players[gameData.CURRENT_TURN].height


def generate_players(player_count: int):
    players = arcade.SpriteList()
    x_offset = gameData.SCREEN_X / player_count
    x_start = gameData.SCREEN_X / (player_count*2)
    for i in range(player_count):
        set_x = (i * x_offset) + x_start
        set_y = gameData.SCREEN_Y / 4.5
        cur_player = Player.Player(image_path="Player_Sprites/P" + str(i + 1) + ".png",
                                   scaling=gameData.PLAYER_SPRITE_SCALING,
                                   money=20, cards=[],
                                   location_x=set_x,
                                   location_y=set_y)

        cur_player.center_x = set_x
        cur_player.center_y = set_y

        players.append(cur_player)

    return players


def generate_card_deck():
    deck = arcade.SpriteList()

    for filename in os.listdir('Card_Sprites'):
        if filename == 'Back.png':
            continue
        file_path = 'Card_Sprites/' + filename

        filename = filename.split('_')
        card_suit = filename[0]
        card_val = get_value_from_card_name(filename[1].split('.')[0])

        cur_card = Card.Card(image_path=file_path,
                             scaling=gameData.CARD_SPRITE_SCALING,
                             suit=card_suit, value=card_val)

        cur_card.center_y = -100
        cur_card.center_x = -100

        deck.append(cur_card)

    return deck


def get_value_from_card_name(value_string: str):
    if value_string == "Jack" or "Queen" or "King":
        return 10
    elif value_string == "Ace":
        return 1
    else:
        return int(value_string)


def shuffle_deck(deck):
    for i in range(len(deck) - 1, 1, -1):
        new_index = random.randint(0, i - 1)

        card_1 = deck[i]
        card_2 = deck[new_index]

        deck.remove(card_1)
        deck.remove(card_2)

        temp_x = card_1.center_x
        temp_y = card_1.center_y

        card_1.center_x = card_2.center_x
        card_1.center_y = card_2.center_y

        card_2.center_x = temp_x
        card_2.center_y = temp_y

        deck.insert(new_index, card_1)
        deck.insert(i, card_2)


def get_screen_dimensions():
    screen_width = None
    screen_height = None

    for m in get_monitors():
        if m.is_primary:
            screen_width = m.width
            screen_height = m.height
            return screen_width, screen_height

    return None


def main():
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
                             gameData.NUM_PLAYERS,
                             "Black Jack")
    game_window.setup()
    game_window.run()


if __name__ == "__main__":
    main()
