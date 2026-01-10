import random
import json

from models import Game, GameNotFoundError, WordAlreadyExists, WordNotFoundError
from views import GameModel

class GamesRepo:
    _games: dict[str, Game]
    _filename = "games.json"

    def __init__(self):
        try:
            self.reload()
        except FileNotFoundError:
            self._games = {}
            self.persist()

    def reload(self):
        self._games = {}
        with open(self._filename, "r") as games_file:
            games_data = json.load(games_file)
            for game_dict in games_data:
                serialized_game = GameModel(**game_dict)
                self._games[serialized_game.id] = serialized_game.to_game()

    def persist(self):
        with open(self._filename, "w") as games_file:
            games_data = [
                GameModel.from_game(game).model_dump()
                for game in self._games.values()
            ]
            json.dump(games_data, games_file)

    def save(self, game: Game):
        self._games[game.id] = game
        self.persist()

    def get(self, game_id: str):
        if game_id not in self._games.keys():
            raise GameNotFoundError()
        return self._games[game_id]


class WordsRepo:
    _words: list[str]
    _filename = "words.txt"

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