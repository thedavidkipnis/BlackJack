import arcade
import arcade.gui
import ButtonStyles as buttonStyles
import GameData as gameData


class UIManager:
    def __init__(self, game):
        self.ui_elements = None
        self.ui_manager = None

        self.game = game

        self.current_turn = None  # is used here to update certain turn based elements when turn switches

        self.turn_pointer = None

    def setup(self):
        self.ui_elements = arcade.SpriteList()

        self.ui_manager = arcade.gui.UIManager()
        self.ui_manager.enable()

        player_action_buttons = arcade.gui.UIBoxLayout()
        self.ui_manager.add(arcade.gui.UIAnchorWidget(align_x=0, align_y=0,
                                                      child=player_action_buttons))

        self.turn_pointer = arcade.Sprite("UI_Sprites/Pointer.png", gameData.UI_SPRITE_SCALING,
                                          center_x=-100, center_y=-100)

        self.ui_elements.append(self.turn_pointer)

        self.current_turn = -1

    def update_pointer(self):
        self.turn_pointer.center_x = self.game.players[self.game.current_turn].center_x
        self.turn_pointer.center_y = self.game.players[self.game.current_turn].center_y - self.game.players[
            self.game.current_turn].height

    def update_player_action_buttons(self):
        if self.current_turn != self.game.current_turn:
            self.current_turn = self.game.current_turn
            player_action_buttons = arcade.gui.UIBoxLayout()
            self.ui_manager.clear()

            stand_button = buttonStyles.PlayerStandButton(text="Stand", width=80, height=35, game=self.game)
            hit_button = buttonStyles.PlayerHitButton(text="Hit", width=80, height=35, game=self.game)
            player_action_buttons.add(stand_button.with_space_around(bottom=20))
            player_action_buttons.add(hit_button)

            new_button_x = self.game.players[self.current_turn].center_x - (gameData.SCREEN_X/2) + 120
            new_button_y = -1 * ((gameData.SCREEN_Y/2) - self.game.players[self.game.current_turn].center_y)

            self.ui_manager.add(arcade.gui.UIAnchorWidget(align_x=new_button_x, align_y=new_button_y,
                                                          child=player_action_buttons))

    def __call__(self):
        return UIManager(game=self.game)
