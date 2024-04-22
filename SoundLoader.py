import pygame


class SoundLoader:
    def __init__(self):
        self.sound_root_path = "sound/"
        self.snd_jk = self.load_jjamggam()
        self.snd_insert = self.load_insert_coin()
        self.snd_bb = self.load_bbo()
        self.snd_win = self.load_win()
        self.snd_lose = self.load_lose()
        self.snd_draw = self.load_draw()
        self.snd_rule = self.load_spinning_roulette()
        self.snd_yap = self.load_yappi()
        self.snd_get_coin = self.load_get_coin()

    def load_jjamggam(self):
        path = self.sound_root_path + "jk.wav"
        return pygame.mixer.Sound(path)

    def load_insert_coin(self):
        path = self.sound_root_path + "insert.wav"
        return pygame.mixer.Sound(path)

    def load_bbo(self):
        path = self.sound_root_path + "bb.wav"
        return pygame.mixer.Sound(path)

    def load_win(self):
        path = self.sound_root_path + "win.wav"
        return pygame.mixer.Sound(path)

    def load_lose(self):
        path = self.sound_root_path + "lose.wav"
        return pygame.mixer.Sound(path)

    def load_draw(self):
        path = self.sound_root_path + "draw.wav"
        return pygame.mixer.Sound(path)

    def load_spinning_roulette(self):
        path = self.sound_root_path + "rule.wav"
        return pygame.mixer.Sound(path)

    def load_yappi(self):
        path = self.sound_root_path + "yap.wav"
        return pygame.mixer.Sound(path)

    def load_get_coin(self):
        path = self.sound_root_path + "get_coin.wav"
        return pygame.mixer.Sound(path)
