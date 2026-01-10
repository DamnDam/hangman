import random
import json

from models import Game, Player
from models import GameNotFoundError, WordAlreadyExists, WordNotFoundError, PlayerNotFoundError
from views import GameModel, PlayerStats

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
    _players_stats: dict[str, PlayerStats]
    _filename: str = "data/players.json"

    def __init__(self, GamesRepo: GamesRepo):
        self._games_repo = GamesRepo
        try:
            self.reload()
        except FileNotFoundError:
            self._players_stats = {}
            self.persist()

    def reload(self):
        self._players_stats = {}
        with open(self._filename, "r") as players_file:
            players_data = json.load(players_file)
            for player_dict in players_data:
                self._players_stats[player_dict["name"]] = PlayerStats(**player_dict)

    
    def persist(self):
        with open(self._filename, "w") as players_file:
            players_data = [
                player_stats.model_dump()
                for player_stats in self._players_stats.values()
            ]
            json.dump(players_data, players_file)

    def get(self, player_name: str) -> Player:
        # Get all games for this player
        games = [
            game_model.to_game()
            for game_model in self._games_repo._game_models.values()
            if game_model.player.name == player_name
        ]
        if not games:
            raise PlayerNotFoundError()
        player_stats = self._players_stats.get(player_name)
        if not player_stats:
            player_stats = PlayerStats(
                name=player_name,
                total_games=0,
                games_won=0,
                games_lost=0,
                ranking=None,
            )
            self._players_stats[player_name] = player_stats
        return Player(
            name=player_name, 
            games=games, 
            total_wins=player_stats.games_won, 
            total_losses=player_stats.games_lost,
            ranking=player_stats.ranking,
        )

    def get_top_players(self, n: int) -> list[PlayerStats]:
        # Sort players by ranking
        sorted_players = sorted(
            self._players_stats.values(),
            key=lambda ps: (ps.ranking if ps.ranking is not None else float('inf'))
        )
        return sorted_players[:n]
        
    def save(self, player: Player, game: Game):
        # User finished a game => update and save player stats
        player.update_score(game)
        self._players_stats[player.name] = PlayerStats.from_player(player)
        # Compute ranking (sorting based on number of wins - number of losses)
        scores = {
            player_stats.name: player_stats.games_won - player_stats.games_lost
            for player_stats in self._players_stats.values()
        }
        sorted_scores = sorted(scores.items(), key=lambda item: item[1], reverse=True)
        # Update ranks
        for rank, (player_name, _) in enumerate(sorted_scores, start=1):
            player_stats = self._players_stats[player_name]
            player_stats.ranking = rank
            self._players_stats[player_name] = player_stats
        self.persist()