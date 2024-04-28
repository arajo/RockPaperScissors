from random import randint


class WinnerCalculator:
    def __init__(self, ):
        self.initial_ring_num = 0
        self.user_win = 12
        self.draw = 14
        self.user_lose = 15
        self.total_ring_num = 11
        self.ring_num = self.initial_ring_num

    def increase_ring_num(self):
        self.ring_num += 1

    def get_winner(self, click_loc):
        res = randint(0, 50)
        if res < 8:
            # user win
            self.ring_num = self.user_win
            cur_hand = click_loc - 1

            if cur_hand < 0:
                cur_hand = 2

        elif res < 30:
            # draw
            self.ring_num = self.draw
            cur_hand = click_loc

        else:
            # user lose
            self.ring_num = self.user_lose
            cur_hand = click_loc + 1
            if cur_hand > 2:
                cur_hand = 0
        return cur_hand

    @staticmethod
    def get_winner_coin(coin_controller):
        """
        우승시 획득 코인 랜덤 선정
        """
        res = randint(0, 342)
        if res < 20:
            get_coin, tg_ring = 4, 0
        elif res < 80:
            get_coin, tg_ring = 1, 1
        elif res < 115:
            get_coin, tg_ring = 2, 2
        elif res < 123:
            get_coin, tg_ring = 7, 3
        elif res < 143:
            get_coin, tg_ring = 4, 4
        elif res < 178:
            get_coin, tg_ring = 2, 5
        elif res < 184:
            get_coin, tg_ring = 20, 6
        elif res < 244:
            get_coin, tg_ring = 1, 7
        elif res < 279:
            get_coin, tg_ring = 2, 8
        elif res < 299:
            get_coin, tg_ring = 4, 9
        elif res < 307:
            get_coin, tg_ring = 7, 10
        else:
            get_coin, tg_ring = 2, 11

        coin_controller.get_coin = get_coin
        return tg_ring
