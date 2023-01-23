import arcade
import arcade.gui
import GameData as gameData

red_style = {
    "font_name": ("calibri", "arial"),
    "font_size": 15,
    "font_color": arcade.color.WHITE,
    "border_width": 2,
    "border_color": arcade.color.BLACK,
    "bg_color": arcade.color.REDWOOD,

    # used if button is pressed
    "bg_color_pressed": arcade.color.WHITE,
    "border_color_pressed": arcade.color.RED,  # also used when hovered
    "font_color_pressed": arcade.color.RED,
}

disabled_button = {
    "font_name": ("calibri", "arial"),
    "font_size": 20,
    "font_color": arcade.color.BLACK,
    "border_width": 2,
    "border_color": arcade.color.GREEN,
    "bg_color": arcade.color.GREEN,

    # used if button is pressed
    "bg_color_pressed": arcade.color.GREEN,
    "border_color_pressed": arcade.color.GREEN,  # also used when hovered
    "font_color_pressed": arcade.color.BLACK,
}


class PlayerStandButton(arcade.gui.UIFlatButton):

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
                 game=None,
                 **kwargs):
        super().__init__(x, y, width, height, text, size_hint, size_hint_min, size_hint_max, style)
        self.game = game

    def on_click(self, event: arcade.gui.UIOnClickEvent):
        self.game.current_turn = (self.game.current_turn + 1) % self.game.num_players


class PlayerHitButton(arcade.gui.UIFlatButton):
    """
    Class for creating a button that lets a player 'hit'.
    """

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
                 game=None,
                 **kwargs):
        super().__init__(x, y, width, height, text, size_hint, size_hint_min, size_hint_max, style)
        self.game = game

    def on_click(self, event: arcade.gui.UIOnClickEvent):
        cur_player = self.game.players[self.game.current_turn]
        self.game.give_player_new_card(cur_player)

        card_count = len(cur_player.cards)
        if card_count < 3:
            x_start = cur_player.center_x - cur_player.cards[0].width
        else:
            x_start = cur_player.center_x - (1.5 * cur_player.cards[0].width)
        for i in range(card_count):
            cur_player.cards[i].center_x = (cur_player.cards[i].width / 2) + x_start + (
                        (i % 3) * cur_player.cards[i].width)
            cur_player.cards[i].center_y = cur_player.center_y + 150 + (cur_player.cards[i].height * (i // 3))

        self.game.check_scores()


class QuitButton(arcade.gui.UIFlatButton):
    """
    Class for creating a button that closes the game.
    """

    def on_click(self, event: arcade.gui.UIOnClickEvent):
        arcade.exit()


class PlayerSelectionButton(arcade.gui.UIFlatButton):
    """
    Class for a set-up window button. When clicked, closes the set-up window and sets the number of players
    for the game, as chosen by the user.
    """

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
