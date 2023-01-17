import arcade
import Card


class Player(arcade.Sprite):
    def __init__(self, image_path: str, scaling: float, money: int, cards, location_x: float, location_y: float):
        super().__init__(image_path, scaling)

        self.texture = arcade.load_texture(image_path)
        self.money = money
        self.cards = cards
        self.location_x = location_x
        self.location_y = location_y

    def __call__(self, image_path, scaling, money, cards, location_x, location_y):
        return Player(image_path=image_path, scaling=scaling, money=money, cards=cards, location_x=location_x, location_y=location_y)

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
