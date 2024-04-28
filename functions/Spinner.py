class Spinner:
    def __init__(self, display, state_controller, hand_controller):
        self.win_led = 0
        self.tg_ring = 0
        self.display = display
        self.state_controller = state_controller
        self.hand_controller = hand_controller

    def spin_and_select(self, time_controller, coin_controller, winner_calculator, key_insert_receptor):
        if time_controller.time_del < time_controller.draw_prize_time:
            time_controller.increase_time()

        if time_controller.time_del == time_controller.draw_prize_time - 1:
            self.tg_ring = winner_calculator.get_winner_coin(coin_controller)

        self.initial_display(coin_controller)

        self.hand_controller.increase_hand_flk()
        if self.hand_controller.hand_flk > self.hand_controller.max_idle_hand_flk:
            self.hand_controller.initiate_hand_flk()
            self.win_led = not self.win_led
            winner_calculator.increase_ring_num()

            if winner_calculator.ring_num > winner_calculator.total_ring_num:
                winner_calculator.__init__()

        self.display.ring_on(self.win_led + 12)
        self.display.ring_on(winner_calculator.ring_num)
        if winner_calculator.ring_num == self.tg_ring and time_controller.time_del == time_controller.draw_prize_time:
            self.display.snd_rule.stop()
            self.display.snd_yap.play()
            time_controller.set_time(-20)
            coin_controller.reset_coin_cnt()
            self.state_controller.give_prize_state()

        if key_insert_receptor.current_loc < key_insert_receptor.return_loc:
            self.display.play_btn(key_insert_receptor.current_loc)
        else:
            self.display.play_btn(4)

    def result(self, time_controller, coin_controller, winner_calculator):
        self.display.background_page()

        time_controller.increase_time()
        if time_controller.time_del == 4 and coin_controller.get_coin > coin_controller.coin_cnt:
            time_controller.__init__()
            coin_controller.generate_coins_image(coin_controller.coin_cnt)
            coin_controller.increase_coins()
            coin_controller.increase_coin_cnt()
            self.display.snd_get_coin.play()

        for i in range(0, coin_controller.coin_cnt):
            self.display.give_coins(coin_controller, i)

        self.result_display(coin_controller, winner_calculator)

        if time_controller.time_del == 30:
            self.state_controller.idle_state()

    def initial_display(self, coin_controller):
        self.display.background_page()
        self.display.print_numbers(coin_controller)
        self.display.start_btn(0)
        self.display.hand_play(self.hand_controller.roulette_hand)

    def result_display(self, coin_controller, winner_calculator):
        self.display.print_numbers(coin_controller)
        self.display.start_btn(0)
        self.display.hand_play(self.hand_controller.roulette_hand)
        self.display.ring_on(self.win_led + 12)
        self.display.ring_on(winner_calculator.ring_num)
        self.display.play_btn(4)
