import pygame
from pygame.locals import Rect

from ImageLoader import ImageLoader


class Display(ImageLoader):
    def __init__(self, params):
        self.SURFACE = pygame.display.set_mode((params["display_width"], params["display_height"]), pygame.FULLSCREEN)
        super().__init__()
        self.ring_x = params["ring_x"]
        self.ring_y = params["ring_y"]

    def start_btn(self, psh):
        self.SURFACE.blit(self.start_btn_img[psh], (479, psh * 3 + 232))

    def play_btn(self, num):
        for i in range(0, 3):
            if i == num:
                self.SURFACE.blit(self.play_btn_img[i * 2 + 1], (i * 148 + 53, 437))
            else:
                self.SURFACE.blit(self.play_btn_img[i * 2], (i * 148 + 53, 431))

    def reset_exit_btn(self, psh, btn_type):
        """
        :param psh: 0 or 1
        :param btn_type: "reset" or "exit"
        :return:
        """
        btn_img = self.reset_btn_img if btn_type == 'reset' else self.exit_btn_img

        if psh:
            self.SURFACE.blit(btn_img, (11, 55))
        else:
            self.SURFACE.blit(btn_img, (11, 59))

    def hand_play(self, num):
        self.SURFACE.blit(self.himg, (141, 168), Rect(num * 195, 0, 195, 195))

    def print_number(self, num, loc):
        tem = 999999
        num = min(num, tem)

        for i in range(0, 7):
            if num > tem:
                self.SURFACE.blit(self.num_img[num // (tem + 1)], (i * 23 + 466, loc * 91 + 93))
                num = num % (tem + 1)
            else:
                self.SURFACE.blit(self.num_img[0], (i * 23 + 466, loc * 91 + 93))

            tem = tem // 10

    def print_numbers(self, coin_controller):
        self.print_number(coin_controller.cumulative_coins * 100, 0)
        self.print_number(coin_controller.current_coins * 100, 1)

    def ring_on(self, num):
        self.SURFACE.blit(self.ring_img[num], (self.ring_x[num], self.ring_y[num]))

    def intro_page(self):
        self.SURFACE.fill((0, 0, 0))
        self.SURFACE.blit(self.logo, self.logo_loc)

    def idle_page(self):
        self.SURFACE.blit(self.bgimg, self.background_loc)

    def background_page(self):
        self.SURFACE.blit(self.bgimg, self.background_loc)

    def give_coins(self, coin_controller, i):
        self.SURFACE.blit(self.coin_img[coin_controller.coin_i[i]],
                          (coin_controller.coin_x[i], coin_controller.coin_y[i]))
