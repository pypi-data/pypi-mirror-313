from cs410_arena.game.go.board import Board, GameState, Move
from cs410_arena.game.go.scoring import compute_game_result
from cs410_arena.game.go.gotypes import Player, Point
import random

class GoGame:
    def __init__(self, board_size=19):
        self.board_size = board_size
        self.game_state = GameState.new_game(self.board_size)
        self.move_history = []

    def play_move(self, move):
        if self.game_state.is_valid_move(move):
            self.game_state = self.game_state.apply_move(move)
            self.move_history.append(move)
            return True
        return False

    def score_game(self):
        return compute_game_result(self.game_state)
        
    def run_match(self, players):
        """
        Run a match between two players.
        Args:
            players: Tuple of (black_player, white_player) where players are GoBot instances
        Returns:
            Match result dictionary
        """
        black_player, white_player = players
        
        # Setup players for the match
        black_player.setup(Player.black)
        white_player.setup(Player.white)
        
        current_player = black_player
        self.move_history = []
        self.game_state = GameState.new_game(self.board_size)
        
        last_move = None
        while not self.game_state.is_over():
            # Update both players with the current state
            black_player.update(self.game_state, last_move)
            white_player.update(self.game_state, last_move)
            
            # Get the current player's move
            move = current_player.get_action(self.game_state)
            
            if move.is_resign:
                return {
                    'winner': white_player if current_player == black_player else black_player,
                    'resigned': True,
                    'moves': len(self.move_history)
                }
                
            if self.play_move(move):
                last_move = move
                current_player = white_player if current_player == black_player else black_player
            
        result = self.score_game()
        return {
            'winner': black_player if result.winner == Player.black else white_player,
            'score': str(result),
            'moves': len(self.move_history)
        }

    
    def generate_sgf(self, match):
        """
        Generate SGF string for the game.
        Args:
            match: Tuple of (black_player, white_player)
        Returns:
            SGF format string
        """
        black_player, white_player = match
        moves_str = ""
        
        for i, move in enumerate(self.move_history):
            color = 'B' if i % 2 == 0 else 'W'
            player = black_player if i % 2 == 0 else white_player
            
            if move.is_pass:
                move_str = "[]"
                moves_str += f";{color}{move_str}C[{player} passes]"
            elif move.is_resign:
                moves_str += f";{color}[]C[{player} resigns]"
                break
            else:
                x = chr(ord('a') + move.point.col - 1)
                y = chr(ord('a') + move.point.row - 1)
                move_str = f"[{x}{y}]"
                moves_str += f";{color}{move_str}"
            
        if self.game_state.is_over():
            result = self.score_game()
            if any(m.is_resign for m in self.move_history):
                winner = white_player if result.winner == Player.white else black_player
                moves_str += f"C[Game ended by resignation. {winner} wins]"
            else:
                moves_str += f"C[Final score: {str(result)}]"
            
        return f"(;FF[4]CA[UTF-8]SZ[{self.board_size}]PB[{black_player}]PW[{white_player}]{moves_str})"
