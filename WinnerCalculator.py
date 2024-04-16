from random import randint


class WinnerCalculator:
    @staticmethod
    def get_winner_coin():
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
        return get_coin, tg_ring

    @staticmethod
    def get_winner(click_loc):
        res = randint(0, 50)
        if res < 8:
            # user win
            ring_num = 12
            cur_hand = click_loc - 1

            if cur_hand < 0:
                cur_hand = 2

        elif res < 30:
            # draw
            ring_num = 14
            cur_hand = click_loc

        else:
            # user lose
            ring_num = 15
            cur_hand = click_loc + 1
            if cur_hand > 2:
                cur_hand = 0
        return cur_hand, ring_num
