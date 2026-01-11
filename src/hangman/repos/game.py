from .base import BaseRepo
from ..models import Game, GameNotFoundError
from ..views import GameModel
from .player import PlayersRepo

class GamesRepo(BaseRepo):
    _repo: dict[str, GameModel]

    _filename = "data/games.json"
    _key_field = "id"
    _model_cls: type = GameModel

    _player_repo: PlayersRepo

    def __init__(self, player_repo: PlayersRepo):
        self._player_repo = player_repo
        super().__init__()

    def save(self, game: Game):
        self._repo[game.id] = GameModel.from_game(game)
        self._persist()

    def get(self, game_id: str) -> Game:
        if game_id not in self._repo.keys():
            raise GameNotFoundError()
        game_model = self._repo[game_id]
        return Game(
            id=game_model.id,
            player=self._player_repo.get(player_name=game_model.player_name, nofail=True),
            max_errors=game_model.max_errors,
            word_to_guess=game_model.word_to_guess,
            errors=game_model.errors,
            selected_letters=game_model.selected_letters,
        )
    
    def list_for_player(self, player_name: str) -> list[Game]:
        return [
            self.get(game_id=game_model.id) 
            for game_model in self._repo.values() 
            if game_model.player_name == player_name
        ]