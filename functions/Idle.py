class Idle:
    def __init__(self, display, state_controller, hand_controller, fps):
        self.fps = fps
        self.display = display
        self.state_controller = state_controller
        self.hand_controller = hand_controller

    def action(self, coin_controller, key_insert_receptor):
        self.display.idle_page()
        self.hand_controller.idle_hand_flk(self.fps)
        self.display.hand_play(self.hand_controller.current_hand)
        self.display.print_numbers(coin_controller)
        self.display.play_btn(4)

        if key_insert_receptor.current_loc == key_insert_receptor.return_loc and coin_controller.current_coins > 0:
            if not coin_controller.coin_pressed:
                self.display.snd_insert.play()
            coin_controller.coin_inserted()
            self.display.start_btn(1)
        else:
            if coin_controller.coin_pressed:
                coin_controller.use_coin()
                self.state_controller.coin_inserted()
                self.display.snd_jk.play()
                self.state_controller.play_state()

            self.display.start_btn(0)
