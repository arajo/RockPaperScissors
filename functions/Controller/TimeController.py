class TimeController:
    def __init__(self):
        self.time_del = 0
        self.draw_prize_time = 60

    def increase_time(self):
        self.time_del += 1

    def set_time(self, i):
        self.time_del = i
