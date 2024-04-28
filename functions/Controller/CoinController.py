from random import randint


class CoinController:
    def __init__(self, params):
        self.current_coins = params["initial_coins"]
        self.cumulative_coins = 0
        self.coin_pressed = False
        self.coin_x = params["coin_x"]
        self.coin_y = params["coin_y"]
        self.coin_i = params["coin_i"]

    def use_coin(self):
        self.coin_pressed = False
        self.cumulative_coins += 1
        self.current_coins -= 1

    def coin_inserted(self):
        self.coin_pressed = True

    def increase_coins(self):
        self.current_coins += 1

    def generate_coins_image(self, coin_cnt):
        self.coin_x[coin_cnt] = randint(475, 565)
        self.coin_y[coin_cnt] = randint(385, 407)
        self.coin_i[coin_cnt] = randint(0, 1)

