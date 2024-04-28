class StateController:
    def __init__(self, mode):
        self.can_play = False
        self.intro_mode = mode["intro"]
        self.idle_mode = mode["idle"]
        self.play_mode = mode["play"]
        self.draw_prize_mode = mode["draw_prize"]
        self.give_prize_mode = mode["give_prize"]
        self.mode = self.intro_mode

    def coin_inserted(self):
        self.can_play = True

    def coin_used(self):
        self.can_play = False

    def idle_state(self):
        self.mode = self.idle_mode

    def play_state(self):
        self.mode = self.play_mode

    def draw_prize_state(self):
        self.mode = self.draw_prize_mode

    def give_prize_state(self):
        self.mode = self.give_prize_mode
