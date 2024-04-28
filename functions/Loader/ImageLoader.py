import pygame


class ImageLoader:
    def __init__(self):
        self.image_root_path = "data/imgs/"
        self.logo_loc = (163, 145)
        self.background_loc = (0, 0)
        self.logo = self.load_logo()
        self.start_btn_img = self.load_start_btn()
        self.ring_img = self.load_roulette()
        self.exit_btn_img = self.load_exit_btn()
        self.play_btn_img = self.load_play_btn()
        self.num_img = self.load_coin_banner_numbers()
        self.bgimg = self.load_background()
        self.himg = self.load_hands()
        self.coin_img = self.load_coins()
        self.reset_btn_img = self.load_reset_btn()

    def load_logo(self):
        path = self.image_root_path + "logo.png"
        return pygame.image.load(path).convert_alpha()

    def load_start_btn(self):
        return [pygame.image.load(self.image_root_path + f"btn_s{i}.png").convert_alpha() for i in range(2)]

    def load_roulette(self):
        numbers = [pygame.image.load(self.image_root_path + f"L{str(i).zfill(2)}.png").convert_alpha() for i in
                   range(12)]
        win_lose = [pygame.image.load(self.image_root_path + f"{w}.png").convert_alpha() for w in
                    ['LWL', 'LWR', 'LDR', 'LLS']]
        return numbers + win_lose

    def load_exit_btn(self):
        path = self.image_root_path + "btn_exit.png"
        return pygame.image.load(path).convert_alpha()

    def load_play_btn(self):
        return [pygame.image.load(self.image_root_path + f"btn_{i}.png").convert_alpha() for i in
                ['00', '01', '10', '11', '20', '21']]

    def load_coin_banner_numbers(self):
        return [pygame.image.load(self.image_root_path + f"n{i}.png").convert_alpha() for i in range(10)]

    def load_background(self):
        path = self.image_root_path + "back_img.jpg"
        return pygame.image.load(path).convert()

    def load_hands(self):
        path = self.image_root_path + "hands.png"
        return pygame.image.load(path).convert_alpha()

    def load_coins(self):
        return [pygame.image.load(self.image_root_path + f"coin{i}.png").convert_alpha() for i in range(2)]

    def load_reset_btn(self):
        path = self.image_root_path + "reset.png"
        return pygame.image.load(path).convert()
