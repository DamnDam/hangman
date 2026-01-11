from .common import GameStatus

class Player:
    def __init__(
            self,
            name: str,
            total_wins: int = 0,
            total_losses: int = 0,
            ranking: int | None = None,
    ):
        self._name = name
        self._total_wins = total_wins
        self._total_losses = total_losses
        self._ranking = ranking

    @property
    def id(self) -> str:
        return self._id

    @property
    def name(self) -> str:
        return self._name
    
    @property
    def total_wins(self) -> int:
        return self._total_wins
    
    @property
    def total_losses(self) -> int:
        return self._total_losses
    
    @property
    def ranking(self) -> int | None:
        return self._ranking
    
    def update_score(self, game_status: GameStatus) -> None:
        if game_status == GameStatus.WON:
            self._total_wins += 1
        elif game_status == GameStatus.LOST:
            self._total_losses += 1