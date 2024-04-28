class Spinner:
    def __init__(self, state_controller, game_controller):
        self.win_led = 0
        self.tg_ring = 0
        self.state_controller = state_controller
        self.game_controller = game_controller

    def spin_and_select(self, key_insert_receptor):
        if self.game_controller.time_controller.time_del < self.game_controller.time_controller.draw_prize_time:
            self.game_controller.time_controller.increase_time()

        if self.game_controller.time_controller.time_del == self.game_controller.time_controller.draw_prize_time - 1:
            self.tg_ring = self.game_controller.winner_calculator.get_winner_coin(self.game_controller.coin_controller)

        self.initial_display(self.game_controller.coin_controller)

        self.game_controller.hand_controller.increase_hand_flk()
        if self.game_controller.hand_controller.hand_flk > self.game_controller.hand_controller.max_idle_hand_flk:
            self.game_controller.hand_controller.initiate_hand_flk()
            self.win_led = not self.win_led
            self.game_controller.winner_calculator.increase_ring_num()

            if self.game_controller.winner_calculator.ring_num > self.game_controller.winner_calculator.total_ring_num:
                self.game_controller.winner_calculator.__init__()

        self.game_controller.display.ring_on(self.win_led + 12)
        self.game_controller.display.ring_on(self.game_controller.winner_calculator.ring_num)
        if self.game_controller.winner_calculator.ring_num == self.tg_ring and \
                self.game_controller.time_controller.time_del == self.game_controller.time_controller.draw_prize_time:
            self.game_controller.display.snd_rule.stop()
            self.game_controller.display.snd_yap.play()
            self.game_controller.time_controller.set_time(-20)
            self.game_controller.coin_controller.reset_coin_cnt()
            self.state_controller.give_prize_state()

        if key_insert_receptor.current_loc < key_insert_receptor.return_loc:
            self.game_controller.display.play_btn(key_insert_receptor.current_loc)
        else:
            self.game_controller.display.play_btn(4)

    def result(self):
        self.game_controller.display.background_page()

        self.game_controller.time_controller.increase_time()
        if self.game_controller.time_controller.time_del == 4 and \
                self.game_controller.coin_controller.get_coin > self.game_controller.coin_controller.coin_cnt:
            self.game_controller.time_controller.__init__()
            self.game_controller.coin_controller.generate_coins_image(self.game_controller.coin_controller.coin_cnt)
            self.game_controller.coin_controller.increase_coins()
            self.game_controller.coin_controller.increase_coin_cnt()
            self.game_controller.display.snd_get_coin.play()

        for i in range(0, self.game_controller.coin_controller.coin_cnt):
            self.game_controller.display.give_coins(self.game_controller.coin_controller, i)

        self.result_display(self.game_controller.coin_controller, self.game_controller.winner_calculator)

        if self.game_controller.time_controller.time_del == 30:
            self.state_controller.idle_state()

    def initial_display(self, coin_controller):
        self.game_controller.display.background_page()
        self.game_controller.display.print_numbers(coin_controller)
        self.game_controller.display.start_btn(0)
        self.game_controller.display.hand_play(self.game_controller.hand_controller.roulette_hand)

    def result_display(self, coin_controller, winner_calculator):
        self.game_controller.display.print_numbers(coin_controller)
        self.game_controller.display.start_btn(0)
        self.game_controller.display.hand_play(self.game_controller.hand_controller.roulette_hand)
        self.game_controller.display.ring_on(self.win_led + 12)
        self.game_controller.display.ring_on(winner_calculator.ring_num)
        self.game_controller.display.play_btn(4)
