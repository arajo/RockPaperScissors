class Play:
    def __init__(self, display, state_controller, hand_controller):
        self.display = display
        self.state_controller = state_controller
        self.hand_controller = hand_controller

    def action(self, coin_controller, key_insert_receptor, winner_calculator, time_controller):
        self.initial_display(coin_controller)

        if key_insert_receptor.current_loc < key_insert_receptor.return_loc:
            # User play key-in
            self.user_input_display(key_insert_receptor.current_loc)

            if self.state_controller.can_play:
                self.state_controller.coin_used()
                self.hand_controller.initiate_hand_flk()
                self.display.snd_bb.play()
                self.hand_controller.roulette_hand = winner_calculator.get_winner(key_insert_receptor.current_loc)

        else:
            self.display.play_btn(4)

        if self.state_controller.can_play:
            self.hand_controller.increase_hand_flk()
            if self.hand_controller.hand_flk >= self.hand_controller.max_idle_hand_flk:
                self.hand_controller.initiate_and_increase()

        else:
            self.hand_controller.increase_hand_flk()
            if self.hand_controller.hand_flk == self.hand_controller.sound_hand_flk:
                self.game_result_sound_play(winner_calculator)

            if self.hand_controller.hand_flk > self.hand_controller.result_hand_flk:
                self.game_result_state_update(time_controller, winner_calculator)

            self.display.ring_on(winner_calculator.ring_num)

        self.display.hand_play(self.hand_controller.roulette_hand)

    def game_result_state_update(self, time_controller, winner_calculator):
        if winner_calculator.ring_num == winner_calculator.user_lose:
            self.state_controller.idle_state()
        elif winner_calculator.ring_num == winner_calculator.draw:
            self.state_controller.coin_inserted()
        else:
            self.state_controller.draw_prize_state()
            self.display.snd_rule.play(loops=-1)
            winner_calculator.__init__()
            time_controller.__init__()

    def game_result_sound_play(self, winner_calculator):
        if winner_calculator.ring_num == winner_calculator.user_lose:
            self.display.snd_lose.play()
        elif winner_calculator.ring_num == winner_calculator.draw:
            self.display.snd_draw.play()
        else:
            self.display.snd_win.play()

    def user_input_display(self, current_loc):
        self.display.snd_jk.stop()
        self.display.snd_draw.stop()
        self.display.play_btn(current_loc)

    def initial_display(self, coin_controller):
        self.display.background_page()
        self.display.print_numbers(coin_controller)
        self.display.start_btn(0)
