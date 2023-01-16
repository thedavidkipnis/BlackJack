import arcade
import arcade.gui
import ButtonStyles as buttonStyles
import GameData as gameData
import Card
from screeninfo import get_monitors
import os
import random


class ShuffleButton(arcade.gui.UIFlatButton):
    def __init__(self, deck: arcade.SpriteList, **kwargs):
        super().__init__(**kwargs)
        self.deck = deck

    def on_click(self, event: arcade.gui.UIOnClickEvent):
        shuffle_deck(self.deck)


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

        self.card_list = None

        arcade.set_background_color(arcade.color.GREEN_YELLOW)

    def setup(self):
        self.card_list = generate_card_deck()
        shuffle_button = ShuffleButton(text="Shuffle", width=150, height=100, deck=self.card_list)

        self.manager.add(
            arcade.gui.UIAnchorWidget(
                align_x=500,
                align_y=-300,
                child=shuffle_button)
        )

    def on_draw(self):
        self.clear()
        arcade.start_render()

        self.manager.draw()
        self.card_list.draw()


def generate_card_deck():
    deck = arcade.SpriteList()

    counter = 0

    for filename in os.listdir('Card_Sprites'):
        if filename == 'Back.png':
            continue
        file_path = 'Card_Sprites/' + filename

        filename = filename.split('_')
        card_suit = filename[0]
        card_val = filename[1].split('.')[0]

        cur_card = Card.Card(image_path=file_path,
                             scaling=gameData.CARD_SPRITE_SCALING,
                             suit=card_suit, value=card_val)

        cur_card.center_y = 200 + (200 * (counter // 22))
        cur_card.center_x = 85 + (40 * (counter % 22))
        counter += 1

        deck.append(cur_card)

    return deck


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
