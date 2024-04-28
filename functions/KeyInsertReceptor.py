import sys
import pygame
from pygame.locals import QUIT, MOUSEBUTTONDOWN, KEYDOWN, K_LEFT, K_DOWN, K_RIGHT, K_RETURN, K_ESCAPE


class KeyInsertReceptor:
    def __init__(self, params):
        self.initial_loc = params["initial_click_location"]  # None
        self.current_loc = self.initial_loc
        self.left_loc = 0                                    # 가위
        self.down_loc = 1                                    # 바위
        self.right_loc = 2                                   # 보
        self.return_loc = 3                                  # insert coin
        self.escape_loc = 4                                  # exit

    @staticmethod
    def exit():
        pygame.quit()
        sys.exit()

    def check_event(self, event):
        if event.type == QUIT:
            self.exit()

        if event.type == MOUSEBUTTONDOWN:
            if event.button == 1:
                self.get_mouse_click_loc()

        if self.current_loc == self.initial_loc:
            if event.type == KEYDOWN:
                self.get_key_loc(event.key)

    def get_key_loc(self, key):
        if key == K_LEFT:
            self.current_loc = self.left_loc
        elif key == K_DOWN:
            self.current_loc = self.down_loc
        elif key == K_RIGHT:
            self.current_loc = self.right_loc
        elif key == K_RETURN:
            self.current_loc = self.return_loc
        elif key == K_ESCAPE:
            self.current_loc = self.escape_loc
        else:
            self.current_loc = self.initial_loc

    def get_mouse_click_loc(self):
        mouse_loc = pygame.mouse.get_pos()

        if 431 < mouse_loc[1] < 476:
            if 52 < mouse_loc[0] < 130:
                self.current_loc = self.left_loc
            elif 199 < mouse_loc[0] < 279:
                self.current_loc = self.down_loc
            elif 348 < mouse_loc[0] < 427:
                self.current_loc = self.right_loc
            else:
                self.current_loc = self.initial_loc
        else:
            if 481 < mouse_loc[0] < 622 and 236 < mouse_loc[1] < 288:
                self.current_loc = self.return_loc

            elif 12 < mouse_loc[0] < 56 and 58 < mouse_loc[1] < 106:
                self.current_loc = self.escape_loc
            else:
                self.current_loc = self.initial_loc
