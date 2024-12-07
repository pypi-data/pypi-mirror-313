from abc import ABC, abstractmethod
from cs410_arena.game.go.gotypes import Player
from cs410_arena.game.go.board import Move, GameState

class GoBot(ABC):
    def __init__(self, name):
        self.name = name
        self.match_data = {}

    def setup(self, player: Player):
        """Called at the start of each match"""
        self.match_data.clear()
        self.match_data['player'] = player
        self.on_match_start()

    def update(self, game_state: GameState, last_move: Move = None):
        """Called after each move is made"""
        self.on_move_made(game_state, last_move)

    def get_action(self, game_state: GameState) -> Move:
        """Main method to get the bot's next move"""
        return self.select_move(game_state)

    def on_match_start(self):
        """Override to add custom match start logic"""
        pass

    def on_move_made(self, game_state: GameState, last_move: Move):
        """Override to add custom move tracking logic"""
        pass

    @abstractmethod
    def select_move(self, game_state: GameState) -> Move:
        """Select a move given the current game state"""
        pass

    def __str__(self):
        return self.name
    
    def __repr__(self):
        return str(self)