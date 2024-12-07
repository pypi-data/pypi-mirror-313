from matchmaker import BaseMatchmaker
import itertools

class RoundRobinMatchmaker(BaseMatchmaker):
    def __init__(self, match_size=2, order_matters=False):
        """
        match_size: Number of players per match.
        order_matters: If True, generates permutations; otherwise, combinations.
        """
        self.match_size = match_size
        self.order_matters = order_matters

    def generate_matches(self, players):
        """
        Generate matches using round-robin logic.
        """
        if self.order_matters:
            return list(itertools.permutations(players, self.match_size))
        else:
            return list(itertools.combinations(players, self.match_size))
