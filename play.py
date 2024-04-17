import sys
import pygame
from pygame.locals import QUIT, MOUSEBUTTONDOWN, Rect, KEYDOWN
from random import randint

from Params import params
from ImageLoader import ImageLoader
from SoundLoader import SoundLoader
from WinnerCalculator import WinnerCalculator
from KeyInsertReceptor import KeyInsertReceptor

pygame.init()

SURFACE = pygame.display.set_mode((params["display_width"], params["display_height"]), pygame.FULLSCREEN)
FPSL = pygame.time.Clock()

# Load images
image_loader = ImageLoader()
logo = image_loader.load_logo()
start_btn_img = image_loader.load_start_btn()
ring_img = image_loader.load_roulette()
exit_btn_img = image_loader.load_exit_btn()
play_btn_img = image_loader.load_play_btn()
num_img = image_loader.load_coin_banner_numbers()
bgimg = image_loader.load_background()
himg = image_loader.load_hands()
coin_img = image_loader.load_coins()
reset_img = image_loader.load_reset_btn()

# Load sounds
sound_loader = SoundLoader()
snd_jk = sound_loader.load_jjamggam()
snd_insert = sound_loader.load_insert_coin()
snd_bb = sound_loader.load_bbo()
snd_win = sound_loader.load_win()
snd_lose = sound_loader.load_lose()
snd_draw = sound_loader.load_draw()
snd_rule = sound_loader.load_spinning_roulette()
snd_yap = sound_loader.load_yappi()
snd_get_coin = sound_loader.load_get_coin()


def num_print(num, loc):
    tem = 999999
    num = min(num, tem)

    for i in range(0, 7):
        if num > tem:
            SURFACE.blit(num_img[num // (tem + 1)], (i * 23 + 466, loc * 91 + 93))
            num = num % (tem + 1)
        else:
            SURFACE.blit(num_img[0], (i * 23 + 466, loc * 91 + 93))

        tem = tem // 10


def start_btn(psh):
    SURFACE.blit(start_btn_img[psh], (479, psh * 3 + 232))


def hand_play(num):
    SURFACE.blit(himg, (141, 168), Rect(num * 195, 0, 195, 195))


def reset_btn(psh):
    if psh:
        SURFACE.blit(reset_img, (11, 55))
    else:
        SURFACE.blit(reset_img, (11, 59))


def exit_btn(psh):
    if psh:
        SURFACE.blit(exit_btn_img, (11, 55))
    else:
        SURFACE.blit(exit_btn_img, (11, 59))


def ring_on(num):
    ring_x = params["ring_x"]
    ring_y = params["ring_y"]
    SURFACE.blit(ring_img[num], (ring_x[num], ring_y[num]))


def play_btn(num):
    for i in range(0, 3):
        if i == num:
            SURFACE.blit(play_btn_img[i * 2 + 1], (i * 148 + 53, 437))
        else:
            SURFACE.blit(play_btn_img[i * 2], (i * 148 + 53, 431))


def main():
    """
    Initialize Params
    """
    coin = params["initial_coins"]
    all_coin, get_coin, coin_cnt = 0, 0, 0
    exit_press, coin_press, win_led, tg_ring = 0, 0, 0, 0
    coin_x, coin_y, coin_i = params["coin_x"], params["coin_y"], params["coin_i"]

    mode = params["mode"]["intro"]
    can_play, initial_time, hand_flk, cur_hand, ring_num, time_del = 0, 0, 0, 0, 0, 0

    while True:

        key_insert_receptor = KeyInsertReceptor()
        click_loc = key_insert_receptor.initial_loc

        for event in pygame.event.get():

            if event.type == QUIT:
                key_insert_receptor.exit()

            if event.type == MOUSEBUTTONDOWN:
                if event.button == 1:
                    click_loc = key_insert_receptor.get_mouse_click_loc()

            if click_loc == key_insert_receptor.initial_loc:
                if event.type == KEYDOWN:
                    click_loc = key_insert_receptor.get_key_loc(event.key)

        if mode == params["mode"]["intro"]:
            # intro
            SURFACE.fill((0, 0, 0))
            SURFACE.blit(logo, (163, 145))

            initial_time += 1
            if initial_time > params["max_initial_time"]:
                mode = params["mode"]["idle"]

        else:
            if mode == params["mode"]["idle"]:
                # idle
                SURFACE.blit(bgimg, (0, 0))

                hand_flk += 1
                if hand_flk >= params["fps"] * 1:
                    hand_flk = 0
                    cur_hand += 1
                    if cur_hand > 2:
                        cur_hand = 0

                hand_play(cur_hand)
                num_print(all_coin * 100, 0)
                num_print(coin * 100, 1)
                play_btn(4)

                if click_loc == 3 and coin > 0:
                    if not coin_press:
                        snd_insert.play()
                    coin_press = 1
                    start_btn(1)
                else:
                    if coin_press:
                        coin_press = 0
                        all_coin += 1
                        coin -= 1
                        can_play = 1
                        snd_jk.play()
                        mode = params["mode"]["play"]

                    start_btn(0)

            elif mode == params["mode"]["play"]:
                # play
                SURFACE.blit(bgimg, (0, 0))
                num_print(all_coin * 100, 0)
                num_print(coin * 100, 1)
                start_btn(0)

                if click_loc < 3:
                    snd_jk.stop()
                    snd_draw.stop()

                    play_btn(click_loc)
                    if can_play:
                        can_play = 0
                        hand_flk = 0
                        snd_bb.play()

                        cur_hand, ring_num = WinnerCalculator.get_winner(click_loc)

                else:
                    play_btn(4)

                if can_play:
                    hand_flk += 1
                    if hand_flk >= 2:
                        hand_flk = 0
                        cur_hand += 1
                        if cur_hand > 2:
                            cur_hand = 0

                else:
                    hand_flk += 1
                    if hand_flk == 7:
                        if ring_num == 15:
                            snd_lose.play()

                        elif ring_num == 14:
                            snd_draw.play()

                        else:
                            snd_win.play()

                    if hand_flk > 23:
                        if ring_num == 15:
                            mode = params["mode"]["idle"]
                        elif ring_num == 14:
                            can_play = 1
                        else:
                            mode = params["mode"]["draw_prize"]
                            snd_rule.play(loops=-1)
                            ring_num = 0
                            time_del = 0

                    ring_on(ring_num)

                hand_play(cur_hand)

            elif mode == params["mode"]["draw_prize"]:
                # choose the number of coins for winner.
                if time_del < 60:
                    time_del += 1

                if time_del == 59:
                    get_coin, tg_ring = WinnerCalculator.get_winner_coin()

                SURFACE.blit(bgimg, (0, 0))
                num_print(all_coin * 100, 0)
                num_print(coin * 100, 1)
                start_btn(0)
                hand_play(cur_hand)

                hand_flk += 1
                if hand_flk > 2:
                    hand_flk = 0
                    win_led = not win_led
                    ring_num += 1

                    if ring_num > 11:
                        ring_num = 0

                ring_on(win_led + 12)
                ring_on(ring_num)
                if ring_num == tg_ring and time_del == 60:
                    snd_rule.stop()
                    snd_yap.play()
                    time_del = -20
                    coin_cnt = 0
                    mode = params["mode"]["give_prize"]

                if click_loc < 3:
                    play_btn(click_loc)
                else:
                    play_btn(4)

            elif mode == params["mode"]["give_prize"]:
                # give the player coins.
                SURFACE.blit(bgimg, (0, 0))

                time_del += 1
                if time_del == 4 and get_coin > coin_cnt:
                    time_del = 0

                    coin_x[coin_cnt] = randint(475, 565)
                    coin_y[coin_cnt] = randint(385, 407)
                    coin_i[coin_cnt] = randint(0, 1)
                    coin_cnt += 1
                    coin += 1
                    snd_get_coin.play()

                for i in range(0, coin_cnt):
                    SURFACE.blit(coin_img[coin_i[i]], (coin_x[i], coin_y[i]))

                num_print(all_coin * 100, 0)
                num_print(coin * 100, 1)
                start_btn(0)
                hand_play(cur_hand)
                ring_on(win_led + 12)
                ring_on(ring_num)
                play_btn(4)

                if time_del == 30:
                    mode = params["mode"]["idle"]

            if click_loc == 4:
                # exit/reset
                exit_press = 1
                if mode == params["mode"]["idle"] and coin == 0:
                    reset_btn(0)

                else:
                    exit_btn(0)

            else:
                if exit_press:
                    if mode == params["mode"]["idle"] and coin == 0:
                        exit_press = 0
                        coin = 20
                        all_coin = 0

                    else:
                        pygame.quit()
                        sys.exit()

                else:
                    if mode == params["mode"]["idle"] and coin == 0:
                        reset_btn(1)

                    else:
                        exit_btn(1)

        pygame.display.flip()
        FPSL.tick(params["fps"])


if __name__ == '__main__':
    main()
