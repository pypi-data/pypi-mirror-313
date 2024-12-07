from abc import ABC, abstractmethod
import pyspiel

class GoBot(ABC):
    def __init__(self, name):
        self.name = name
        self.match_data = {}

    def setup(self, player: int):
        """Called at the start of each match"""
        self.match_data.clear()
        self.match_data['player'] = player
        self.on_match_start()

    def update(self, game_state: pyspiel.State, last_move: int = None):
        """Called after each move is made"""
        self.on_move_made(game_state, last_move)

    def get_action(self, game_state: pyspiel.State) -> int:
        """Main method to get the bot's next move"""
        return self.select_move(game_state)

    def on_match_start(self):
        """Override to add custom match start logic"""
        pass

    def on_move_made(self, game_state: pyspiel.State, last_move: int):
        """Override to add custom move tracking logic"""
        pass

    @abstractmethod
    def select_move(self, game_state: pyspiel.State) -> int:
        """Select a move given the current game state"""
        pass

    def __str__(self):
        return self.name
    
    def __repr__(self):
        return str(self)