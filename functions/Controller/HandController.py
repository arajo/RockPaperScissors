class HandController:
    def __init__(self):
        self.hand_flk = 0
        self.current_hand = 0
        self.max_idle_hand_flk = 2
        self.sound_hand_flk = 7
        self.result_hand_flk = 23

    def increase_hand_flk(self):
        self.hand_flk += 1

    def initiate_hand_flk(self):
        self.hand_flk = 0

    def increase_current_hand(self):
        self.current_hand += 1
        if self.current_hand > 2:
            self.current_hand = 0

    def initiate_and_increase(self):
        self.initiate_hand_flk()
        self.increase_current_hand()

    def idle_hand_flk(self, fps):
        self.increase_hand_flk()
        if self.hand_flk >= fps * 1:
            self.initiate_and_increase()

