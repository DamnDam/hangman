import random
import json

from models import Game, Player
from models import GameNotFoundError, WordAlreadyExists, WordNotFoundError, PlayerNotFoundError
from views import GameModel, PlayerModel

class GamesRepo:
    _game_models: dict[str, Game]
    _filename = "data/games.json"

    def __init__(self):
        try:
            self.reload()
        except FileNotFoundError:
            self._game_models = {}
            self.persist()

    def reload(self):
        self._game_models = {}
        with open(self._filename, "r") as games_file:
            games_data = json.load(games_file)
            for game_dict in games_data:
                self._game_models[game_dict["id"]] = GameModel(**game_dict)

    def persist(self):
        with open(self._filename, "w") as games_file:
            games_data = [
                game_model.model_dump()
                for game_model in self._game_models.values()
            ]
            json.dump(games_data, games_file)

    def save(self, game: Game):
        self._game_models[game.id] = GameModel.from_game(game)
        self.persist()

    def get(self, game_id: str) -> Game:
        if game_id not in self._game_models.keys():
            raise GameNotFoundError()
        return self._game_models[game_id].to_game()

class WordsRepo:
    _words: list[str]
    _filename = "data/words.txt"

    def __init__(self):
        self.reload()

    def reload(self):
        with open(self._filename, "r") as words_file:
            self._words = [word[:-1] for word in words_file]
    
    def persist(self):
        with open(self._filename, "w") as words_file:
            for word in self._words:
                words_file.write(f"{word}\n")

    def get_random_word(self) -> str:
        return random.choice(self._words)

    def add_word(self, word: str):
        if word in self._words:
            raise WordAlreadyExists()
        self._words.append(word)
        self.persist()
    
    def delete_word(self, word: str):
        if word not in self._words:
            raise WordNotFoundError()
        self._words.remove(word)
        self.persist()


class PlayerRepo:
    _games_repo: GamesRepo
    _players: dict[str, Player]

    def __init__(self, GamesRepo: GamesRepo):
        self._games_repo = GamesRepo

    def reload(self):
        raise NotImplementedError()
    
    def persist(self):
        raise NotImplementedError()

    def get(self, player_name: str) -> Player:
        # Get all games for this player
        games = list(filter(lambda g: g.player.name == player_name, self._games_repo._games.values()))
        if not games:
            raise PlayerNotFoundError()
        return Player(name=player_name, games=games)
    
    def save(self, player: Player):
        raise NotImplementedError()