import sys
import pygame
from pygame.locals import QUIT, MOUSEBUTTONDOWN, Rect, KEYDOWN

from CoinController import CoinController
from HandController import HandController
from Params import params
from ImageLoader import ImageLoader
from SoundLoader import SoundLoader
from WinnerCalculator import WinnerCalculator
from KeyInsertReceptor import KeyInsertReceptor

pygame.init()

SURFACE = pygame.display.set_mode((params["display_width"], params["display_height"]), pygame.FULLSCREEN)
FPSL = pygame.time.Clock()

# Load images and sounds
image_loader = ImageLoader()
sound_loader = SoundLoader()


def num_print(num, loc):
    tem = 999999
    num = min(num, tem)

    for i in range(0, 7):
        if num > tem:
            SURFACE.blit(image_loader.num_img[num // (tem + 1)], (i * 23 + 466, loc * 91 + 93))
            num = num % (tem + 1)
        else:
            SURFACE.blit(image_loader.num_img[0], (i * 23 + 466, loc * 91 + 93))

        tem = tem // 10


def start_btn(psh):
    SURFACE.blit(image_loader.start_btn_img[psh], (479, psh * 3 + 232))


def hand_play(num):
    SURFACE.blit(image_loader.himg, (141, 168), Rect(num * 195, 0, 195, 195))


def reset_exit_btn(psh, btn_type):
    """
    :param psh: 0 or 1
    :param btn_type: "reset" or "exit"
    :return:
    """
    btn_img = image_loader.reset_btn_img if btn_type == 'reset' else image_loader.exit_btn_img

    if psh:
        SURFACE.blit(btn_img, (11, 55))
    else:
        SURFACE.blit(btn_img, (11, 59))


def ring_on(num):
    SURFACE.blit(image_loader.ring_img[num], (params["ring_x"][num], params["ring_y"][num]))


def play_btn(num):
    for i in range(0, 3):
        if i == num:
            SURFACE.blit(image_loader.play_btn_img[i * 2 + 1], (i * 148 + 53, 437))
        else:
            SURFACE.blit(image_loader.play_btn_img[i * 2], (i * 148 + 53, 431))


def main():
    """
    Initialize Params
    """
    get_coin, coin_cnt = 0, 0
    coin_controller = CoinController(params)
    exit_press, win_led, tg_ring = 0, 0, 0

    mode = params["mode"]["intro"]
    can_play, initial_time, ring_num, time_del = 0, 0, 0, 0
    hand_controller = HandController()

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
            SURFACE.blit(image_loader.logo, image_loader.logo_loc)

            initial_time += 1
            if initial_time > params["max_initial_time"]:
                mode = params["mode"]["idle"]

        else:
            if mode == params["mode"]["idle"]:
                # idle
                SURFACE.blit(image_loader.bgimg, image_loader.background_loc)

                hand_controller.increase_hand_flk()
                if hand_controller.hand_flk >= params["fps"] * 1:
                    hand_controller.initiate_and_increase()

                hand_play(hand_controller.current_hand)
                num_print(coin_controller.cumulative_coins * 100, 0)
                num_print(coin_controller.current_coins * 100, 1)
                play_btn(4)

                if click_loc == 3 and coin_controller.current_coins > 0:
                    if not coin_controller.coin_pressed:
                        sound_loader.snd_insert.play()
                    coin_controller.coin_inserted()
                    start_btn(1)
                else:
                    if coin_controller.coin_pressed:
                        coin_controller.use_coin()
                        can_play = 1
                        sound_loader.snd_jk.play()
                        mode = params["mode"]["play"]

                    start_btn(0)

            elif mode == params["mode"]["play"]:
                # play
                SURFACE.blit(image_loader.bgimg, image_loader.background_loc)
                num_print(coin_controller.cumulative_coins * 100, 0)
                num_print(coin_controller.current_coins * 100, 1)
                start_btn(0)

                if click_loc < 3:
                    sound_loader.snd_jk.stop()
                    sound_loader.snd_draw.stop()

                    play_btn(click_loc)
                    if can_play:
                        can_play = 0
                        hand_controller.initiate_hand_flk()
                        sound_loader.snd_bb.play()

                        hand_controller.current_hand, ring_num = WinnerCalculator.get_winner(click_loc)

                else:
                    play_btn(4)

                if can_play:
                    hand_controller.increase_hand_flk()
                    if hand_controller.hand_flk >= 2:
                        hand_controller.initiate_and_increase()

                else:
                    hand_controller.increase_hand_flk()
                    if hand_controller.hand_flk == 7:
                        if ring_num == 15:
                            sound_loader.snd_lose.play()

                        elif ring_num == 14:
                            sound_loader.snd_draw.play()

                        else:
                            sound_loader.snd_win.play()

                    if hand_controller.hand_flk > 23:
                        if ring_num == 15:
                            mode = params["mode"]["idle"]
                        elif ring_num == 14:
                            can_play = 1
                        else:
                            mode = params["mode"]["draw_prize"]
                            sound_loader.snd_rule.play(loops=-1)
                            ring_num = 0
                            time_del = 0

                    ring_on(ring_num)

                hand_play(hand_controller.current_hand)

            elif mode == params["mode"]["draw_prize"]:
                # choose the number of coins for winner.
                if time_del < 60:
                    time_del += 1

                if time_del == 59:
                    get_coin, tg_ring = WinnerCalculator.get_winner_coin()

                SURFACE.blit(image_loader.bgimg, image_loader.background_loc)
                num_print(coin_controller.cumulative_coins * 100, 0)
                num_print(coin_controller.current_coins * 100, 1)
                start_btn(0)
                hand_play(hand_controller.current_hand)

                hand_controller.increase_hand_flk()
                if hand_controller.hand_flk > 2:
                    hand_controller.initiate_hand_flk()
                    win_led = not win_led
                    ring_num += 1

                    if ring_num > 11:
                        ring_num = 0

                ring_on(win_led + 12)
                ring_on(ring_num)
                if ring_num == tg_ring and time_del == 60:
                    sound_loader.snd_rule.stop()
                    sound_loader.snd_yap.play()
                    time_del = -20
                    coin_cnt = 0
                    mode = params["mode"]["give_prize"]

                if click_loc < 3:
                    play_btn(click_loc)
                else:
                    play_btn(4)

            elif mode == params["mode"]["give_prize"]:
                # give the player coins.
                SURFACE.blit(image_loader.bgimg, image_loader.background_loc)

                time_del += 1
                if time_del == 4 and get_coin > coin_cnt:
                    time_del = 0
                    coin_controller.generate_coins_image(coin_cnt)
                    coin_controller.increase_coins()
                    coin_cnt += 1
                    sound_loader.snd_get_coin.play()

                for i in range(0, coin_cnt):
                    SURFACE.blit(image_loader.coin_img[coin_controller.coin_i[i]],
                                 (coin_controller.coin_x[i], coin_controller.coin_y[i]))

                num_print(coin_controller.cumulative_coins * 100, 0)
                num_print(coin_controller.current_coins * 100, 1)
                start_btn(0)
                hand_play(hand_controller.current_hand)
                ring_on(win_led + 12)
                ring_on(ring_num)
                play_btn(4)

                if time_del == 30:
                    mode = params["mode"]["idle"]

            if click_loc == 4:
                # exit/reset
                exit_press = 1
                if mode == params["mode"]["idle"] and coin_controller.current_coins == 0:
                    reset_exit_btn(0, 'reset')

                else:
                    reset_exit_btn(0, 'exit')

            else:
                if exit_press:
                    if mode == params["mode"]["idle"] and coin_controller.current_coins == 0:
                        exit_press = 0
                        coin_controller.__init__(params)

                    else:
                        pygame.quit()
                        sys.exit()

                else:
                    if mode == params["mode"]["idle"] and coin_controller.current_coins == 0:
                        reset_exit_btn(1, 'reset')

                    else:
                        reset_exit_btn(1, 'exit')

        pygame.display.flip()
        FPSL.tick(params["fps"])


if __name__ == '__main__':
    main()
