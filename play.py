import pygame

from Params import params
from functions.Controller.CoinController import CoinController
from functions.Controller.HandController import HandController
from functions.Controller.StateController import StateController
from functions.Controller.TimeController import TimeController
from functions.Display import Display
from functions.Idle import Idle
from functions.Intro import Intro
from functions.KeyInsertReceptor import KeyInsertReceptor
from functions.Play import Play
from functions.Spinner import Spinner
from functions.WinnerCalculator import WinnerCalculator

pygame.init()
FPSL = pygame.time.Clock()
display = Display(params)


def main():
    """
    Initialize Params
    """
    exit_pressed, fps = False, params["fps"]

    coin_controller = CoinController(params)
    hand_controller, winner_calculator, time_controller = HandController(), WinnerCalculator(), TimeController()
    state_controller = StateController(params["mode"])
    intro = Intro(display, state_controller, params["max_initial_time"])
    idle = Idle(display, state_controller, hand_controller, fps)
    play = Play(display, state_controller, hand_controller)
    spinner = Spinner(display, state_controller, hand_controller)

    while True:
        key_insert_receptor = KeyInsertReceptor(params)
        for event in pygame.event.get():
            key_insert_receptor.check_event(event)

        if state_controller.mode == state_controller.intro_mode:
            intro.action()

        else:
            if state_controller.mode == state_controller.idle_mode:
                idle.action(coin_controller, key_insert_receptor)

            elif state_controller.mode == state_controller.play_mode:
                play.action(coin_controller, key_insert_receptor, winner_calculator, time_controller)

            elif state_controller.mode == state_controller.draw_prize_mode:
                # choose the number of coins for winner.
                spinner.select(time_controller, coin_controller, winner_calculator, key_insert_receptor)

            elif state_controller.mode == state_controller.give_prize_mode:
                # give the player coins.
                spinner.give(time_controller, coin_controller, winner_calculator)

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
