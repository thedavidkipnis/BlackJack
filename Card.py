import arcade


class Card(arcade.Sprite):

    def __init__(self, image_path: str, scaling: float, suit: str, value: int):
        super().__init__(image_path, scaling)

        self.texture = arcade.load_texture(image_path)
        self.suit = suit
        self.value = value

    def __call__(self, image_path, scaling, suit, value):
        return Card(image_path=image_path, scaling=scaling, suit=suit, value=value)

    def get_suit(self):
        return self.suit

    def get_value(self):
        return self.value
