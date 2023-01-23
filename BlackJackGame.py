import arcade
import GameData as gameData
import Player
import Card
import os
import random


def generate_players(player_count: int) -> arcade.SpriteList:
    """
    Creates and populates GameWindow's list of players.

    :param player_count: how many players the user picked for this game
    :return: list of Sprites
    """
    players = arcade.SpriteList()
    x_offset = gameData.SCREEN_X / player_count
    x_start = gameData.SCREEN_X / (player_count * 2)
    for i in range(player_count):
        set_x = (i * x_offset) + x_start
        set_y = gameData.SCREEN_Y / 4.5
        cur_player = Player.Player(image_path="Player_Sprites/P" + str(i + 1) + ".png",
                                   scaling=gameData.PLAYER_SPRITE_SCALING,
                                   money=20, cards=[],
                                   can_play_this_round=True,
                                   location_x=set_x,
                                   location_y=set_y)

        cur_player.center_x = set_x
        cur_player.center_y = set_y

        players.append(cur_player)

    return players


def generate_dealer():
    dealer_draw = arcade.SpriteList()
    dealer = Player.Dealer(image_path="Player_Sprites/Dealer.png",
                           scaling=gameData.PLAYER_SPRITE_SCALING,
                           money=20, cards=[],
                           can_play_this_round=True,
                           location_x=gameData.SCREEN_X / 2,
                           location_y=gameData.SCREEN_Y / 2)
    dealer.center_x = gameData.SCREEN_X / 2
    dealer.center_y = gameData.SCREEN_Y

    dealer_draw.append(dealer)

    return dealer_draw, dealer


def generate_card_deck() -> arcade.SpriteList:
    """
    Creates and populates GameWindow's list of cards.

    :return: list of Sprites
    """
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


def get_value_from_card_name(value_string: str) -> int:
    """
    Returns a card's numerical value based on Black Jack rules:
    > Non-face cards: value on card
    > Jack, Queen, King: 10
    > Ace: 1 or 11. Returns 1 by default

    :param value_string: the filename from which the card came
    :return: int representation of given card's value
    """
    if value_string in ["Jack", "Queen", "King"]:
        return 10
    elif value_string == "Ace":
        return 1
    else:
        return int(value_string)


def shuffle_deck(deck):
    """
    Shuffles GameWindow's card deck using Fihser-Yates shuffle.

    :param deck: SpriteList
    """
    for i in range(len(deck) - 1, 1, -1):
        new_index = random.randint(0, i - 1)

        card_1 = deck[i]
        card_2 = deck[new_index]

        deck.remove(card_1)
        deck.remove(card_2)

        deck.insert(new_index, card_1)
        deck.insert(i, card_2)


class Game:

    def __init__(self):
        self.num_players = None
        self.players = None
        self.card_list = None
        self.current_turn = None
        self.current_deck_index = None
        self.dealer = None
        self.dealer_draw = None

    def setup(self, num_players):
        self.num_players = num_players
        self.players = generate_players(num_players)
        self.card_list = generate_card_deck()

        self.dealer_draw, self.dealer = generate_dealer()

        self.current_turn = 0

        self.current_deck_index = 0

        self.new_round()

    def new_round(self):
        shuffle_deck(self.card_list)

        # Setting players' cards
        for player in self.players:
            card_1 = self.card_list[self.current_deck_index]
            card_2 = self.card_list[self.current_deck_index + 1]
            self.current_deck_index += 2
            player.cards = [card_1, card_2]

            card_1.center_x = player.center_x - card_1.width / 2
            card_1.center_y = player.center_y + 150
            card_2.center_x = player.center_x + card_2.width / 2
            card_2.center_y = player.center_y + 150

        # Setting dealer's cards
        dealer_card_1 = self.card_list[self.current_deck_index]
        dealer_card_2 = self.card_list[self.current_deck_index + 1]
        self.current_deck_index += 2
        self.dealer.cards = [dealer_card_1, dealer_card_2]

        dealer_card_1.center_x = self.dealer.center_x - 50
        dealer_card_2.center_x = self.dealer.center_x + 50
        dealer_card_1.center_y = self.dealer.center_y - 150
        dealer_card_2.center_y = self.dealer.center_y - 150

        dealer_down_card = Card.Card(image_path="Card_Sprites/Back.png",
                                     scaling=gameData.CARD_SPRITE_SCALING,
                                     suit="None", value=-1)
        dealer_down_card.center_x = dealer_card_1.center_x
        dealer_down_card.center_y = dealer_card_1.center_y

        self.dealer_draw.append(dealer_down_card)

    def check_scores(self):
        # TODO: implement to check scores at the end of every 'hit' action
        for player in self.players:
            pass

    def give_player_new_card(self, player):
        player.cards.append(self.card_list[self.current_deck_index])
        self.current_deck_index += 1

    def __call__(self):
        return Game()
