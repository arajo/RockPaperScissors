import pygame

from Params import params
from functions.Controller.GameController import GameController
from functions.Controller.StateController import StateController
from functions.KeyInsertReceptor import KeyInsertReceptor
from functions.State.Idle import Idle
from functions.State.Intro import Intro
from functions.State.Play import Play
from functions.State.Spinner import Spinner

pygame.init()
FPSL = pygame.time.Clock()


def main():
    """
    Initialize Params
    """
    exit_pressed, fps = False, params["fps"]

    state_controller = StateController(params["mode"])
    game_controller = GameController(params)

    intro = Intro(game_controller, state_controller, params["max_initial_time"])

    game_controller.initiate_game()
    idle = Idle(state_controller, game_controller, fps)

    game_controller.play_start()
    play = Play(state_controller, game_controller)
    spinner = Spinner(state_controller, game_controller)

    while True:
        key_insert_receptor = KeyInsertReceptor(params)
        for event in pygame.event.get():
            key_insert_receptor.check_event(event)

        if state_controller.mode == state_controller.intro_mode:
            intro.action()

        else:
            if state_controller.mode == state_controller.idle_mode:
                idle.action(key_insert_receptor)

            elif state_controller.mode == state_controller.play_mode:
                play.action(key_insert_receptor)

            elif state_controller.mode == state_controller.draw_prize_mode:
                # choose the number of coins for winner.
                spinner.spin_and_select(key_insert_receptor)

            elif state_controller.mode == state_controller.give_prize_mode:
                # give the player coins.
                spinner.result()

            # exit/reset
            if exit_pressed:
                if state_controller.mode == state_controller.idle_mode and \
                        game_controller.coin_controller.current_coins == 0:
                    exit_pressed = False
                    game_controller.coin_controller.__init__(params)
                else:
                    key_insert_receptor.exit()

            if key_insert_receptor.current_loc == key_insert_receptor.escape_loc:
                exit_pressed = True

            if state_controller.mode == state_controller.idle_mode and \
                    game_controller.coin_controller.current_coins == 0:
                game_controller.display.reset_exit_btn(exit_pressed, 0)
            else:
                game_controller.display.reset_exit_btn(exit_pressed, 1)

        pygame.display.flip()
        FPSL.tick(fps)


if __name__ == '__main__':
    main()
