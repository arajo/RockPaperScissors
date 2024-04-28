from functions.Controller.CoinController import CoinController
from functions.Controller.HandController import HandController
from functions.Controller.TimeController import TimeController
from functions.Display import Display
from functions.WinnerCalculator import WinnerCalculator


class GameController:
    def __init__(self, params):
        self.params = params
        self.hand_controller = None
        self.coin_controller = None
        self.time_controller = None
        self.winner_calculator = None
        self.display = Display(params)

    def initiate_game(self):
        self.coin_controller = CoinController(self.params)
        self.hand_controller = HandController()

    def play_start(self):
        self.winner_calculator = WinnerCalculator()
        self.time_controller = TimeController()


