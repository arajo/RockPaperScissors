class StateController:
    def __init__(self):
        self.can_play = False

    def coin_inserted(self):
        self.can_play = True

    def coin_used(self):
        self.can_play = False
