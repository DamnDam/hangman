from .base import BaseRepo
from ..models import Game, GameStatus, GameNotFoundError
from ..schemas import GameModel
from .player import PlayersRepo

class GamesRepo(BaseRepo):
    _data: dict[str, GameModel]

    _filename = "data/games.json"
    _key_field = "id"
    _BaseSchema: type = GameModel
    _NotFoundException = GameNotFoundError

    _player_repo: PlayersRepo

    def __init__(self, player_repo: PlayersRepo):
        self._player_repo = player_repo
        super().__init__()

    def to_model(self, item: GameModel) -> Game:
        return Game(
            id=item.id,
            player=self._player_repo[item.player_name],
            max_errors=item.max_errors,
            word_to_guess=item.word_to_guess,
            errors=item.errors,
            selected_letters=item.selected_letters,
        )

    def list_for_player(self, player_name: str, game_status: GameStatus | None = None) -> list[Game]:
        return [
            self.to_model(game_model)
            for game_model in self._data.values() 
            if game_model.player_name == player_name 
            and (game_status is None or game_model.game_status == game_status)
        ]