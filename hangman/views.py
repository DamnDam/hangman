from pydantic import BaseModel
from models import Game, GameStatus, Player


class PlayerModel(BaseModel):
    name: str
    games: list["GameModel"]

    @staticmethod
    def from_player(player: 'Player') -> 'PlayerModel':
        return PlayerModel(
            name=player.name,
            games=[GameModel.from_game(game) for game in player.games],
        )
    
    def to_player(self) -> 'Player':
        return Player(
            name=self.name,
            games=[game_model.to_game() for game_model in self.games],
        )

class GameModel(BaseModel):
    id: str
    player: PlayerModel
    max_errors: int
    word_to_guess: str
    errors: int
    selected_letters: list[str]
    word_so_far: str
    errors_left: int
    game_status: GameStatus

    @staticmethod
    def from_game(game: Game) -> 'GameModel':
        return GameModel(
            id=game.id,
            player=PlayerModel.from_player(game.player),
            max_errors=game.max_errors,
            word_to_guess=game.word_to_guess,
            errors=game.errors,
            selected_letters=game.selected_letters,
            word_so_far=game.word_so_far,
            errors_left=game.errors_left,
            game_status=game.game_status,
        )
    
    def to_game(self) -> 'Game':
        return Game(
            id=self.id,
            player=self.player.to_player(),
            max_errors=self.max_errors,
            word_to_guess=self.word_to_guess,
            errors=self.errors,
            selected_letters=self.selected_letters,
        )

class GamePublic(BaseModel):
    id: str
    player_name: str
    max_errors: int
    word_so_far: str
    word_to_guess: str|None
    errors_left: int
    game_status: GameStatus

    @staticmethod
    def from_game(game: Game) -> 'GamePublic':
        return GamePublic(
            id=game.id,
            player_name=game.player.name,
            max_errors=game.max_errors,
            word_so_far=game.word_so_far,
            word_to_guess=game.word_to_guess if game.game_status != GameStatus.IN_PROGRESS else None,
            errors_left=game.errors_left,
            game_status=game.game_status,
        )

class PlayerPublic(BaseModel):
    name: str
    active_games: list[GamePublic]
    total_games: int
    games_won: int
    games_lost: int
    ranking: int | None

    @staticmethod
    def from_player(player: 'Player') -> 'PlayerPublic':
        
        return PlayerPublic(
            name=player.name,
            active_games = [GamePublic.from_game(game) for game in player.games if game.game_status == GameStatus.IN_PROGRESS],
            total_games = len(player.games),
            games_won = player.total_wins,
            games_lost = player.total_losses,
            ranking = player.ranking,
        )
    
class PlayerStats(BaseModel):
    name: str
    total_games: int
    games_won: int
    games_lost: int
    ranking: int | None = None

    @staticmethod
    def from_player(player: 'Player') -> 'PlayerStats':
        return PlayerStats(
            name=player.name,
            total_games=len(player.games),
            games_won=player.total_wins,
            games_lost=player.total_losses,
            ranking=player.ranking,
        )
    
class GameCreation(BaseModel):
    player_name: str
    max_errors: int = 5

class Letter(BaseModel):
    letter: str

class Word(BaseModel):
    word: str
