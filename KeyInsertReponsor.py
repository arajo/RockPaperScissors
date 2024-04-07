import sys
import pygame

from pygame.locals import K_LEFT, K_DOWN, K_RIGHT, K_RETURN, K_ESCAPE


class KeyInsertResponsor:
    """
    click_loc : 0(가위), 1(주먹), 2(보), 3(insert coin), 4(exit)
    """

    @staticmethod
    def exit():
        pygame.quit()
        sys.exit()

    @staticmethod
    def get_key_loc(key):
        if key == K_LEFT:
            return 0
        elif key == K_DOWN:
            return 1
        elif key == K_RIGHT:
            return 2
        elif key == K_RETURN:
            return 3
        elif key == K_ESCAPE:
            return 4

    @staticmethod
    def get_mouse_click_loc():
        mouse_loc = pygame.mouse.get_pos()

        if 431 < mouse_loc[1] < 476:
            if 52 < mouse_loc[0] < 130:
                return 0
            elif 199 < mouse_loc[0] < 279:
                return 1
            elif 348 < mouse_loc[0] < 427:
                return 2
        else:
            if 481 < mouse_loc[0] < 622 and 236 < mouse_loc[1] < 288:
                return 3

            if 12 < mouse_loc[0] < 56 and 58 < mouse_loc[1] < 106:
                return 4
