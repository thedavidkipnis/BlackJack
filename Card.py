import arcade


class Card(arcade.Sprite):

    def __init__(self, image_path, scaling, suit, value):
        super().__init__(image_path, scaling)

        self.texture = arcade.load_texture(image_path)
        self.suit = suit
        self.value = value

    def __call__(self, image_path, scaling, suit, value):
        return Card(image_path=image_path, scaling=scaling, suit=suit, value=value)
