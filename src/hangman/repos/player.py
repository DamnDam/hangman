from .base import BaseRepo
from ..models import Player, GameStatus
from ..models import PlayerNotFoundError
from ..schemas import PlayerModel

class PlayersRepo(BaseRepo):
    _data: dict[str, PlayerModel]
    
    _filename: str = "data/players.json"
    _key_field: str = "name"
    _BaseSchema: type = PlayerModel
    _NotFoundException = PlayerNotFoundError

    def to_model(self, item: PlayerModel) -> Player:
        return Player(
            name=item.name,
            total_wins=item.games_won,
            total_losses=item.games_lost,
            ranking=item.ranking,
        )

    def get_top_players(self, n: int) -> list[PlayerModel]:
        return list(self._data.values())[:n]
        
    def save_result(self, player: Player, game_status: GameStatus):
        # User finished a game => update and save player stats
        player.update_score(game_status)
        self._data[player.name] = PlayerModel.from_model(player)
        # Compute ranking (sorting based on number of wins - number of losses)
        scores = {
            player_model.name: player_model.games_won - player_model.games_lost
            for player_model in self._data.values()
        }
        sorted_scores = sorted(scores.items(), key=lambda item: item[1], reverse=True)
        # Update ranks
        for rank, (player_name, _) in enumerate(sorted_scores, start=1):
            player_model = self._data[player_name]
            player_model.ranking = rank
            self._data[player_name] = player_model
        sorted_players = sorted(
            self._data.values(),
            key=lambda player_model: 
                player_model.ranking if player_model.ranking is not None 
                else float('-inf')
        )
        self._data = {
            player_model.name: player_model
            for player_model in sorted_players
        }
        self._persist()