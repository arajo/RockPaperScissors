class Idle:
    def __init__(self, state_controller, game_controller, fps):
        self.fps = fps
        self.state_controller = state_controller
        self.game_controller = game_controller

    def action(self, key_insert_receptor):
        self.initial_display(self.game_controller.coin_controller)

        if key_insert_receptor.current_loc == key_insert_receptor.return_loc and self.game_controller.coin_controller.current_coins > 0:
            if not self.game_controller.coin_controller.coin_pressed:
                self.game_controller.display.snd_insert.play()
            self.game_controller.coin_controller.coin_inserted()
            self.game_controller.display.start_btn(1)
        else:
            if self.game_controller.coin_controller.coin_pressed:
                self.game_controller.coin_controller.use_coin()
                self.state_controller.coin_inserted()
                self.game_controller.display.snd_jk.play()
                self.state_controller.play_state()

            self.game_controller.display.start_btn(0)

    def initial_display(self, coin_controller):
        self.game_controller.display.idle_page()
        self.game_controller.hand_controller.idle_hand_flk(self.fps)
        self.game_controller.display.hand_play(self.game_controller.hand_controller.roulette_hand)
        self.game_controller.display.print_numbers(coin_controller)
        self.game_controller.display.play_btn(4)
