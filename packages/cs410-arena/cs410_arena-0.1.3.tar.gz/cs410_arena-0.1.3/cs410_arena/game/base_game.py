from abc import ABC, abstractmethod

class BaseGame(ABC):
    """
    Abstract base class for all games.
    """

    @abstractmethod
    def run_match(self, players):
        """
        Run a single match and return detailed results.
        Args:
            players: List of players.
        Returns:
            dict: Match results, including placements.
        """
        pass
