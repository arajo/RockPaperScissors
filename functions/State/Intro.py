class Intro:
    def __init__(self, game_controller, state_controller, max_initial_time):
        self.initiate_time = 0
        self.max_initial_time = max_initial_time
        self.state_controller = state_controller
        self.game_controller = game_controller

    def action(self):
        self.initial_display()

        self.initiate_time += 1
        if self.initiate_time > self.max_initial_time:
            self.state_controller.idle_state()

    def initial_display(self):
        self.game_controller.display.intro_page()
