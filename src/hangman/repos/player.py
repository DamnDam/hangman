from .base import BaseRepo
from ..models import Player, GameStatus
from ..models import PlayerNotFoundError
from ..views import PlayerModel

class PlayersRepo(BaseRepo):
    _repo: dict[str, PlayerModel]
    
    _filename: str = "data/players.json"
    _key_field: str = "name"
    _model_cls: type = PlayerModel

    def get(self, player_name: str, nofail=False) -> Player:
        player_model = self._repo.get(player_name)
        if not player_model:
            if nofail:
                return Player(name=player_name)
            raise PlayerNotFoundError()
        return Player(
            name=player_name, 
            total_wins=player_model.games_won, 
            total_losses=player_model.games_lost,
            ranking=player_model.ranking,
        )

    def get_top_players(self, n: int) -> list[PlayerModel]:
        return [player_model for player_model in list(self._repo.values())][:n]
        
    def save_result(self, player: Player, game_status: GameStatus):
        # User finished a game => update and save player stats
        player.update_score(game_status)
        self._repo[player.name] = PlayerModel.from_player(player)
        # Compute ranking (sorting based on number of wins - number of losses)
        scores = {
            player_model.name: player_model.games_won - player_model.games_lost
            for player_model in self._repo.values()
        }
        sorted_scores = sorted(scores.items(), key=lambda item: item[1], reverse=True)
        # Update ranks
        for rank, (player_name, _) in enumerate(sorted_scores, start=1):
            player_model = self._repo[player_name]
            player_model.ranking = rank
            self._repo[player_name] = player_model
        sorted_players = sorted(
            self._repo.values(),
            key=lambda player_model: 
                player_model.ranking if player_model.ranking is not None 
                else float('-inf')
        )
        self._repo = {
            player_model.name: player_model
            for player_model in sorted_players
        }
        self._persist()