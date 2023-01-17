import arcade
import Card

"""
Class representing a Player object in the game.
"""


class Player(arcade.Sprite):
    def __init__(self, image_path: str, scaling: float, money: int, cards,
                 can_play_this_round: bool, location_x: float, location_y: float):
        super().__init__(image_path, scaling)

        self.texture = arcade.load_texture(image_path)
        self.money = money
        self.cards = cards
        self.location_x = location_x
        self.location_y = location_y
        self.can_play_this_round = can_play_this_round

    def __call__(self, image_path, scaling, money, cards, can_play_this_round, location_x, location_y):
        return Player(image_path=image_path, scaling=scaling, money=money, cards=cards,
                      can_play_this_round=can_play_this_round, location_x=location_x, location_y=location_y)

    # Getter/Setter methods
    def get_money(self):
        return self.money

    def set_money(self, money: int):
        self.money = money

    def get_cards(self):
        return self.cards

    def set_cards(self, cards):
        self.cards = cards

    def add_card(self, card: Card):
        self.cards.append(card)

    def set_turn(self, can_play: bool):
        self.can_play_this_round = can_play
