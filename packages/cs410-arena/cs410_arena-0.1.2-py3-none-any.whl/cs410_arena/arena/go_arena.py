import requests
from typing import Dict, List
import time
from ..game.go.board import Move, GameState
from ..game.go.gotypes import Player

class GoArena:
    def __init__(self, bot_urls: Dict[str, str], board_size: int = 19):
        """
        Args:
            bot_urls: Dictionary mapping bot names to their API URLs
            board_size: Size of the Go board
        """
        self.bot_urls = bot_urls
        self.board_size = board_size
        self.timeout = 5  # seconds per move

    def setup_bot(self, bot_url: str, player: Player) -> bool:
        try:
            response = requests.post(
                f"{bot_url}/setup",
                json={'player': player.name},
                timeout=self.timeout
            )
            return response.status_code == 200
        except requests.exceptions.RequestException as e:
            print(f"Error setting up bot at {bot_url}: {e}")
            return False

    def get_bot_move(self, bot_url: str, game_state: GameState) -> Move:
        try:
            response = requests.post(
                f"{bot_url}/get_move",
                json=game_state.to_dict(),
                timeout=self.timeout
            )
            move_data = response.json()['move']
            return Move.from_dict(move_data)
        except requests.exceptions.RequestException as e:
            print(f"Error getting move from bot at {bot_url}: {e}")
            return Move.resign()

    def run_match(self, black_bot_url: str, white_bot_url: str) -> dict:
        """Run a single match between two bots"""
        from ..game.go.go_game import GoGame
        game = GoGame(self.board_size)
        
        if not (self.setup_bot(black_bot_url, Player.black) and 
                self.setup_bot(white_bot_url, Player.white)):
            return {'error': 'Failed to setup bots'}

        current_bot_url = black_bot_url
        while not game.is_over():
            move = self.get_bot_move(current_bot_url, game.game_state)
            
            if move.is_resign:
                return {
                    'winner': 'white' if current_bot_url == black_bot_url else 'black',
                    'resigned': True,
                    'moves': len(game.move_history)
                }
                
            game.play_move(move)
            current_bot_url = white_bot_url if current_bot_url == black_bot_url else black_bot_url

        result = game.score_game()
        return {
            'winner': 'black' if result.winner == Player.black else 'white',
            'score': str(result),
            'moves': len(game.move_history)
        }

    def run_tournament(self) -> List[dict]:
        """Run a round-robin tournament between all bots"""
        results = []
        bot_names = list(self.bot_urls.keys())
        
        for i, black_bot in enumerate(bot_names):
            for white_bot in bot_names[i+1:]:
                print(f"\nStarting match: {black_bot} (B) vs {white_bot} (W)")
                result = self.run_match(
                    self.bot_urls[black_bot],
                    self.bot_urls[white_bot]
                )
                result.update({
                    'black': black_bot,
                    'white': white_bot
                })
                results.append(result)
                print(f"Result: {result}")
                
                # Play reverse match (switch colors)
                print(f"\nStarting match: {white_bot} (B) vs {black_bot} (W)")
                result = self.run_match(
                    self.bot_urls[white_bot],
                    self.bot_urls[black_bot]
                )
                result.update({
                    'black': white_bot,
                    'white': black_bot
                })
                results.append(result)
                print(f"Result: {result}")
                
                # Small delay between matches
                time.sleep(1)
                
        return results
