import random
import json
import shutil

from .models import Game, Player
from .models import GameNotFoundError, WordAlreadyExists, WordNotFoundError, PlayerNotFoundError
from .views import PlayerModel, GameModel

class PlayerRepo:
    _players: dict[str, PlayerModel]
    _filename: str = "data/players.json"

    def __init__(self,):
        try:
            self.reload()
        except FileNotFoundError:
            self._players = {}
            self.persist()

    def reload(self):
        self._players = {}
        with open(self._filename, "r") as players_file:
            players_data = json.load(players_file)
            for player_dict in players_data:
                self._players[player_dict["name"]] = PlayerModel(**player_dict)
    
    def persist(self):
        with open(self._filename, "w") as players_file:
            players_data = [
                player_model.model_dump()
                for player_model in self._players.values()
            ]
            json.dump(players_data, players_file)

    def get(self, player_name: str, nofail=False) -> Player:
        player_model = self._players.get(player_name)
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
        return [player_model for player_model in list(self._players.values())][:n]
        
    def save(self, player: Player, game: Game):
        # User finished a game => update and save player stats
        player.update_score(game)
        self._players[player.name] = PlayerModel.from_player(player)
        # Compute ranking (sorting based on number of wins - number of losses)
        scores = {
            player_model.name: player_model.games_won - player_model.games_lost
            for player_model in self._players.values()
        }
        sorted_scores = sorted(scores.items(), key=lambda item: item[1], reverse=True)
        # Update ranks
        for rank, (player_name, _) in enumerate(sorted_scores, start=1):
            player_model = self._players[player_name]
            player_model.ranking = rank
            self._players[player_name] = player_model
        sorted_players = sorted(
            self._players.values(),
            key=lambda player_model: 
                player_model.ranking if player_model.ranking is not None 
                else float('-inf')
        )
        self._players = {
            player_model.name: player_model
            for player_model in sorted_players
        }
        self.persist()

class GamesRepo:
    _player_repo: PlayerRepo
    _games: dict[str, GameModel]
    _filename = "data/games.json"

    def __init__(self, player_repo: PlayerRepo):
        self._player_repo = player_repo
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
                self._games[game_dict["id"]] = GameModel(**game_dict)

    def persist(self):
        with open(self._filename, "w") as games_file:
            games_data = [
                game_model.model_dump()
                for game_model in self._games.values()
            ]
            json.dump(games_data, games_file)

    def save(self, game: Game):
        self._games[game.id] = GameModel.from_game(game)
        self.persist()

    def get(self, game_id: str) -> Game:
        if game_id not in self._games.keys():
            raise GameNotFoundError()
        game_model = self._games[game_id]
        return Game(
            id=game_model.id,
            player=self._player_repo.get(player_name=game_model.player_name, nofail=True),
            max_errors=game_model.max_errors,
            word_to_guess=game_model.word_to_guess,
            errors=game_model.errors,
            selected_letters=game_model.selected_letters,
        )
    
    def get_for_player(self, player: Player) -> list[Game]:
        return [
            self.get(game_id=game_model.id) 
            for game_model in self._games.values() 
            if game_model.player_name == player.name
        ]

class WordsRepo:
    _words: list[str]
    _filename = "data/words.txt"

    def __init__(self):
        try:
            self.reload()
        except FileNotFoundError:
            shutil.copy("words.txt", self._filename)
            self.reload()

    def reload(self):
        with open(self._filename, "r") as words_file:
            self._words = [word[:-1] for word in words_file]
    
    def persist(self):
        with open(self._filename, "w") as words_file:
            for word in self._words:
                words_file.write(f"{word}\n")

    def get_random_word(self, word_length: int | None = None) -> str:
        if word_length is not None:
            filtered_words = [word for word in self._words if len(word) == word_length]
            if filtered_words:
                return random.choice(filtered_words)
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


