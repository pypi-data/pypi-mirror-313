import requests
from typing import Dict, List
import numpy as np
import pyspiel

class GoArena:
    def __init__(self, bot_urls: Dict[str, str], board_size: int = 19):
        """
        Args:
            bot_urls: Dictionary mapping bot names to their API URLs
            board_size: Size of the Go board
        """
        self.bot_urls = bot_urls
        self.board_size = board_size
        self.timeout = 5
        self.game = pyspiel.load_game("go", {"board_size": board_size})

    def setup_bot(self, bot_url: str, player: int) -> bool:
        try:
            response = requests.post(
                f"{bot_url}/setup",
                json={'player': player},
                timeout=self.timeout
            )
            return response.status_code == 200
        except requests.exceptions.RequestException as e:
            print(f"Error setting up bot at {bot_url}: {e}")
            return False

    def get_bot_move(self, bot_url: str, game_state: pyspiel.State) -> int:
        try:
            response = requests.post(
                f"{bot_url}/get_move",
                json={'game_state': game_state.to_dict()},
                timeout=self.timeout
            )
            move_data = response.json()['move']
            return move_data
        except requests.exceptions.RequestException as e:
            print(f"Error getting move from bot at {bot_url}: {e}")
            return -1  # Assuming -1 is an invalid move

    def run_match(self, black_bot_url: str, white_bot_url: str) -> dict:
        """Run a single match between two bots"""
        state = self.game.new_initial_state()
        
        if not (self.setup_bot(black_bot_url, 0) and 
                self.setup_bot(white_bot_url, 1)):
            return {'error': 'Failed to setup bots'}

        current_bot_url = black_bot_url
        while not state.is_terminal():
            move = self.get_bot_move(current_bot_url, state)
            
            if move == -1:
                return {
                    'winner': 'white' if current_bot_url == black_bot_url else 'black',
                    'resigned': True,
                    'moves': state.num_moves()
                }
                
            state.apply_action(move)
            current_bot_url = white_bot_url if current_bot_url == black_bot_url else black_bot_url

        result = state.returns()
        return {
            'winner': 'black' if result[0] > 0 else 'white',
            'score': str(result),
            'moves': state.num_moves()
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
                
        return results
