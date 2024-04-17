class SoundLoader:
    def __init__(self):
        self.sound_root_path = "sound/"

    def load_jjamggam(self):
        return self.sound_root_path + "jk.wav"

    def load_insert_coin(self):
        return self.sound_root_path + "insert.wav"

    def load_bbo(self):
        return self.sound_root_path + "bb.wav"

    def load_win(self):
        return self.sound_root_path + "win.wav"

    def load_lose(self):
        return self.sound_root_path + "lose.wav"

    def load_draw(self):
        return self.sound_root_path + "draw.wav"

    def load_spinning_roulette(self):
        return self.sound_root_path + "rule.wav"

    def load_yappi(self):
        return self.sound_root_path + "yap.wav"

    def load_get_coin(self):
        return self.sound_root_path + "get_coin.wav"

