
from random import randint


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




