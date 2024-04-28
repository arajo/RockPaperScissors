class Play:
    def __init__(self, state_controller, game_controller):
        self.state_controller = state_controller
        self.game_controller = game_controller

    def action(self, key_insert_receptor):
        self.initial_display(self.game_controller.coin_controller)

        if key_insert_receptor.current_loc < key_insert_receptor.return_loc:
            # User play key-in
            self.user_input_display(key_insert_receptor.current_loc)

            if self.state_controller.can_play:
                self.state_controller.coin_used()
                self.game_controller.hand_controller.initiate_hand_flk()
                self.game_controller.display.snd_bb.play()
                self.game_controller.hand_controller.roulette_hand = self.game_controller.winner_calculator.get_winner(
                    key_insert_receptor.current_loc)

        else:
            self.game_controller.display.play_btn(4)

        if self.state_controller.can_play:
            self.game_controller.hand_controller.increase_hand_flk()
            if self.game_controller.hand_controller.hand_flk >= self.game_controller.hand_controller.max_idle_hand_flk:
                self.game_controller.hand_controller.initiate_and_increase()

        else:
            self.game_controller.hand_controller.increase_hand_flk()
            if self.game_controller.hand_controller.hand_flk == self.game_controller.hand_controller.sound_hand_flk:
                self.game_result_sound_play(self.game_controller.winner_calculator)

            if self.game_controller.hand_controller.hand_flk > self.game_controller.hand_controller.result_hand_flk:
                self.game_result_state_update(self.game_controller.time_controller,
                                              self.game_controller.winner_calculator)

            self.game_controller.display.ring_on(self.game_controller.winner_calculator.ring_num)

        self.game_controller.display.hand_play(self.game_controller.hand_controller.roulette_hand)

    def game_result_state_update(self, time_controller, winner_calculator):
        if winner_calculator.ring_num == winner_calculator.user_lose:
            self.state_controller.idle_state()
        elif winner_calculator.ring_num == winner_calculator.draw:
            self.state_controller.coin_inserted()
        else:
            self.state_controller.draw_prize_state()
            self.game_controller.display.snd_rule.play(loops=-1)
            winner_calculator.__init__()
            time_controller.__init__()

    def game_result_sound_play(self, winner_calculator):
        if winner_calculator.ring_num == winner_calculator.user_lose:
            self.game_controller.display.snd_lose.play()
        elif winner_calculator.ring_num == winner_calculator.draw:
            self.game_controller.display.snd_draw.play()
        else:
            self.game_controller.display.snd_win.play()

    def user_input_display(self, current_loc):
        self.game_controller.display.snd_jk.stop()
        self.game_controller.display.snd_draw.stop()
        self.game_controller.display.play_btn(current_loc)

    def initial_display(self, coin_controller):
        self.game_controller.display.background_page()
        self.game_controller.display.print_numbers(coin_controller)
        self.game_controller.display.start_btn(0)
