from models import Game

class GamesRepo:
    _games: dict[str, Game]

    def __init__(self):
        self._games = {}

    def save(self, game: Game):
        self._games[game.id] = game

    def get(self, game_id: str):
        if game_id not in self._games.keys():
            raise ValueError(f"Game with id {game_id} not found")
        return self._games[game_id]