import sys
import pygame
from pygame.locals import QUIT, MOUSEBUTTONDOWN, KEYDOWN

from CoinController import CoinController
from Display import Display
from HandController import HandController
from KeyInsertReceptor import KeyInsertReceptor
from Params import params
from SoundLoader import SoundLoader
from WinnerCalculator import WinnerCalculator

pygame.init()
FPSL = pygame.time.Clock()
sound_loader = SoundLoader()
display = Display(params)


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
            display.intro_page()

            initial_time += 1
            if initial_time > params["max_initial_time"]:
                mode = params["mode"]["idle"]

        else:
            if mode == params["mode"]["idle"]:
                # idle
                display.idle_page()

                hand_controller.increase_hand_flk()
                if hand_controller.hand_flk >= params["fps"] * 1:
                    hand_controller.initiate_and_increase()

                display.hand_play(hand_controller.current_hand)
                display.num_print(coin_controller.cumulative_coins * 100, 0)
                display.num_print(coin_controller.current_coins * 100, 1)
                display.play_btn(4)

                if click_loc == 3 and coin_controller.current_coins > 0:
                    if not coin_controller.coin_pressed:
                        sound_loader.snd_insert.play()
                    coin_controller.coin_inserted()
                    display.start_btn(1)
                else:
                    if coin_controller.coin_pressed:
                        coin_controller.use_coin()
                        can_play = 1
                        sound_loader.snd_jk.play()
                        mode = params["mode"]["play"]

                    display.start_btn(0)

            elif mode == params["mode"]["play"]:
                # play
                display.background_page()
                display.num_print(coin_controller.cumulative_coins * 100, 0)
                display.num_print(coin_controller.current_coins * 100, 1)
                display.start_btn(0)

                if click_loc < 3:
                    sound_loader.snd_jk.stop()
                    sound_loader.snd_draw.stop()

                    display.play_btn(click_loc)
                    if can_play:
                        can_play = 0
                        hand_controller.initiate_hand_flk()
                        sound_loader.snd_bb.play()

                        hand_controller.current_hand, ring_num = WinnerCalculator.get_winner(click_loc)

                else:
                    display.play_btn(4)

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

                    display.ring_on(ring_num)

                display.hand_play(hand_controller.current_hand)

            elif mode == params["mode"]["draw_prize"]:
                # choose the number of coins for winner.
                if time_del < 60:
                    time_del += 1

                if time_del == 59:
                    get_coin, tg_ring = WinnerCalculator.get_winner_coin()

                display.background_page()
                display.num_print(coin_controller.cumulative_coins * 100, 0)
                display.num_print(coin_controller.current_coins * 100, 1)
                display.start_btn(0)
                display.hand_play(hand_controller.current_hand)

                hand_controller.increase_hand_flk()
                if hand_controller.hand_flk > 2:
                    hand_controller.initiate_hand_flk()
                    win_led = not win_led
                    ring_num += 1

                    if ring_num > 11:
                        ring_num = 0

                display.ring_on(win_led + 12)
                display.ring_on(ring_num)
                if ring_num == tg_ring and time_del == 60:
                    sound_loader.snd_rule.stop()
                    sound_loader.snd_yap.play()
                    time_del = -20
                    coin_cnt = 0
                    mode = params["mode"]["give_prize"]

                if click_loc < 3:
                    display.play_btn(click_loc)
                else:
                    display.play_btn(4)

            elif mode == params["mode"]["give_prize"]:
                # give the player coins.
                display.background_page()

                time_del += 1
                if time_del == 4 and get_coin > coin_cnt:
                    time_del = 0
                    coin_controller.generate_coins_image(coin_cnt)
                    coin_controller.increase_coins()
                    coin_cnt += 1
                    sound_loader.snd_get_coin.play()

                for i in range(0, coin_cnt):
                    display.give_coins(coin_controller, i)

                display.num_print(coin_controller.cumulative_coins * 100, 0)
                display.num_print(coin_controller.current_coins * 100, 1)
                display.start_btn(0)
                display.hand_play(hand_controller.current_hand)
                display.ring_on(win_led + 12)
                display.ring_on(ring_num)
                display.play_btn(4)

                if time_del == 30:
                    mode = params["mode"]["idle"]

            if click_loc == 4:
                # exit/reset
                exit_press = 1
                if mode == params["mode"]["idle"] and coin_controller.current_coins == 0:
                    display.reset_exit_btn(0, 'reset')

                else:
                    display.reset_exit_btn(0, 'exit')

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
                        display.reset_exit_btn(1, 'reset')

                    else:
                        display.reset_exit_btn(1, 'exit')

        pygame.display.flip()
        FPSL.tick(params["fps"])


if __name__ == '__main__':
    main()
