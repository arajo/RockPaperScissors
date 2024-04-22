class HandController:
    def __init__(self):
        self.hand_flk = 0
        self.current_hand = 0

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

