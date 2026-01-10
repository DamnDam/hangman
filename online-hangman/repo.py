import random

from models import Game, WordAlreadyExists



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


class WordsRepo:
    _words: list[str]

    def __init__(self):
        with open("words.txt", "r") as words_file:
            self._words = [word[:-1] for word in words_file]

    def get_random_word(self) -> str:
        return random.choice(self._words)

    def add_word(self, word: str):
        if word in self._words:
            raise WordAlreadyExists()
        self._words.append(word)