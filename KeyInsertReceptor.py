import sys
import pygame

from pygame.locals import K_LEFT, K_DOWN, K_RIGHT, K_RETURN, K_ESCAPE


class KeyInsertReceptor:
    """
    click_loc : 0(가위), 1(주먹), 2(보), 3(insert coin), 4(exit), 9(None)
    """

    def __init__(self, params):
        self.initial_loc = params["initial_click_location"]
        self.current_loc = self.initial_loc

    @staticmethod
    def exit():
        pygame.quit()
        sys.exit()

    def get_key_loc(self, key):
        if key == K_LEFT:
            self.current_loc = 0
        elif key == K_DOWN:
            self.current_loc = 1
        elif key == K_RIGHT:
            self.current_loc = 2
        elif key == K_RETURN:
            self.current_loc = 3
        elif key == K_ESCAPE:
            self.current_loc = 4
        else:
            self.current_loc = self.initial_loc

    def get_mouse_click_loc(self):
        mouse_loc = pygame.mouse.get_pos()

        if 431 < mouse_loc[1] < 476:
            if 52 < mouse_loc[0] < 130:
                self.current_loc = 0
            elif 199 < mouse_loc[0] < 279:
                self.current_loc = 1
            elif 348 < mouse_loc[0] < 427:
                self.current_loc = 2
            else:
                self.current_loc = self.initial_loc
        else:
            if 481 < mouse_loc[0] < 622 and 236 < mouse_loc[1] < 288:
                self.current_loc = 3

            elif 12 < mouse_loc[0] < 56 and 58 < mouse_loc[1] < 106:
                self.current_loc = 4
            else:
                self.current_loc = self.initial_loc
