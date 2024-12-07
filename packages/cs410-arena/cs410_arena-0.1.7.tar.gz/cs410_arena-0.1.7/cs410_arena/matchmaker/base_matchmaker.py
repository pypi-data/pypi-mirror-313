from abc import ABC, abstractmethod

class BaseMatchmaker(ABC):
    """
    Abstract base class for all matchmakers.
    """

    @abstractmethod
    def generate_matches(self, players):
        """
        Generate a list of matches from the given players.
        Args:
            players: List of players (e.g., ["Player 1", "Player 2", ...]).
        Returns:
            List of matches, where each match is a tuple of players.
        """
        pass