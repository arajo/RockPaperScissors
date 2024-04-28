import sys
import pygame

from CoinController import CoinController
from Display import Display
from HandController import HandController
from KeyInsertReceptor import KeyInsertReceptor
from Params import params
from SoundLoader import SoundLoader
from StateController import StateController
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
    initiate_time, time_del = 0, 0
    win_led, tg_ring = 0, 0
    coin_controller = CoinController(params)
    exit_pressed, fps = False, params["fps"]

    hand_controller = HandController()
    state_controller = StateController(params["mode"])
    winner_calculator = WinnerCalculator()

    while True:
        key_insert_receptor = KeyInsertReceptor(params)
        for event in pygame.event.get():
            key_insert_receptor.check_event(event)

        if state_controller.mode == state_controller.intro_mode:
            # intro
            display.intro_page()

            initiate_time += 1
            if initiate_time > params["max_initial_time"]:
                state_controller.idle_state()

        else:
            if state_controller.mode == state_controller.idle_mode:
                # idle
                display.idle_page()
                hand_controller.idle_hand_flk(fps)
                display.hand_play(hand_controller.current_hand)
                display.print_numbers(coin_controller)
                display.play_btn(4)

                if key_insert_receptor.current_loc == key_insert_receptor.return_loc and coin_controller.current_coins > 0:
                    if not coin_controller.coin_pressed:
                        sound_loader.snd_insert.play()
                    coin_controller.coin_inserted()
                    display.start_btn(1)
                else:
                    if coin_controller.coin_pressed:
                        coin_controller.use_coin()
                        state_controller.coin_inserted()
                        sound_loader.snd_jk.play()
                        state_controller.play_state()

                    display.start_btn(0)

            elif state_controller.mode == state_controller.play_mode:
                # play
                display.background_page()
                display.print_numbers(coin_controller)
                display.start_btn(0)

                if key_insert_receptor.current_loc < key_insert_receptor.return_loc:
                    # User play key-in
                    sound_loader.snd_jk.stop()
                    sound_loader.snd_draw.stop()
                    display.play_btn(key_insert_receptor.current_loc)

                    if state_controller.can_play:
                        state_controller.coin_used()
                        hand_controller.initiate_hand_flk()
                        sound_loader.snd_bb.play()
                        hand_controller.current_hand = winner_calculator.get_winner(key_insert_receptor.current_loc)

                else:
                    display.play_btn(4)

                if state_controller.can_play:
                    hand_controller.increase_hand_flk()
                    if hand_controller.hand_flk >= hand_controller.max_idle_hand_flk:
                        hand_controller.initiate_and_increase()

                else:
                    hand_controller.increase_hand_flk()
                    if hand_controller.hand_flk == hand_controller.sound_hand_flk:
                        if winner_calculator.ring_num == winner_calculator.user_lose:
                            sound_loader.snd_lose.play()
                        elif winner_calculator.ring_num == winner_calculator.draw:
                            sound_loader.snd_draw.play()
                        else:
                            sound_loader.snd_win.play()

                    if hand_controller.hand_flk > hand_controller.result_hand_flk:
                        if winner_calculator.ring_num == winner_calculator.user_lose:
                            state_controller.idle_state()
                        elif winner_calculator.ring_num == winner_calculator.draw:
                            state_controller.coin_inserted()
                        else:
                            state_controller.draw_prize_state()
                            sound_loader.snd_rule.play(loops=-1)
                            winner_calculator.__init__()
                            time_del = 0

                    display.ring_on(winner_calculator.ring_num)

                display.hand_play(hand_controller.current_hand)

            elif state_controller.mode == state_controller.draw_prize_mode:
                # choose the number of coins for winner.
                if time_del < 60:
                    time_del += 1

                if time_del == 59:
                    get_coin, tg_ring = WinnerCalculator.get_winner_coin()

                display.background_page()
                display.print_numbers(coin_controller)
                display.start_btn(0)
                display.hand_play(hand_controller.current_hand)

                hand_controller.increase_hand_flk()
                if hand_controller.hand_flk > hand_controller.max_idle_hand_flk:
                    hand_controller.initiate_hand_flk()
                    win_led = not win_led
                    winner_calculator.increase_ring_num()

                    if winner_calculator.ring_num > winner_calculator.total_ring_num:
                        winner_calculator.__init__()

                display.ring_on(win_led + 12)
                display.ring_on(winner_calculator.ring_num)
                if winner_calculator.ring_num == tg_ring and time_del == 60:
                    sound_loader.snd_rule.stop()
                    sound_loader.snd_yap.play()
                    time_del = -20
                    coin_cnt = 0
                    state_controller.give_prize_state()

                if key_insert_receptor.current_loc < key_insert_receptor.return_loc:
                    display.play_btn(key_insert_receptor.current_loc)
                else:
                    display.play_btn(4)

            elif state_controller.mode == state_controller.give_prize_mode:
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

                display.print_numbers(coin_controller)
                display.start_btn(0)
                display.hand_play(hand_controller.current_hand)
                display.ring_on(win_led + 12)
                display.ring_on(winner_calculator.ring_num)
                display.play_btn(4)

                if time_del == 30:
                    state_controller.idle_state()

            # exit/reset
            if exit_pressed:
                if state_controller.mode == state_controller.idle_mode and coin_controller.current_coins == 0:
                    exit_pressed = False
                    coin_controller.__init__(params)
                else:
                    key_insert_receptor.exit()

            if key_insert_receptor.current_loc == key_insert_receptor.escape_loc:
                exit_pressed = True

            if state_controller.mode == state_controller.idle_mode and coin_controller.current_coins == 0:
                display.reset_exit_btn(exit_pressed, 0)
            else:
                display.reset_exit_btn(exit_pressed, 1)

        pygame.display.flip()
        FPSL.tick(fps)


if __name__ == '__main__':
    main()
