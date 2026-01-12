from pydantic import BaseModel

from .models import Game, GameStatus, Player

class BaseSchema(BaseModel):
    class Config:
        extra = 'allow'

class PlayerBase(BaseSchema):
    name: str

class PlayerModel(PlayerBase):
    games_won: int
    games_lost: int
    ranking: int | None = None

    @staticmethod
    def from_player(player: 'Player') -> 'PlayerModel':
        return PlayerModel(
            name=player.name,
            games_won=player.total_wins,
            games_lost=player.total_losses,
            ranking=player.ranking,
        )

class PlayerEnum(PlayerModel):
    pass

class PlayerPublic(PlayerEnum):
    active_games: list["GameEnum"]

    @staticmethod
    def from_player(player: 'Player', active_games: list[Game]) -> 'PlayerPublic':
        return PlayerPublic(
            name=player.name,
            games_won=player.total_wins,
            games_lost=player.total_losses,
            ranking=player.ranking,
            active_games=[GameEnum.from_game(game=game) for game in active_games],
        )

class GameCreation(BaseSchema):
    player_name: str
    max_errors: int = 5
    word_length: int | None = None

class GameBase(GameCreation):
    id: str
    word_to_guess: str | None = None
    word_so_far: str
    errors_left: int
    game_status: GameStatus

class GameModel(GameBase):
    word_to_guess: str # Mandatory in internal model
    errors: int
    selected_letters: list[str]

    @staticmethod
    def from_game(game: Game) -> 'GameModel':
        return GameModel(
            id=game.id,
            player_name=game.player.name,
            max_errors=game.max_errors,
            word_to_guess=game.word_to_guess,
            errors=game.errors,
            selected_letters=game.selected_letters,
            word_so_far=game.word_so_far,
            errors_left=game.errors_left,
            game_status=game.game_status,
        )

class GameEnum(GameBase):
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

class GamePublic(GameEnum):
    pass

class Letter(BaseSchema):
    letter: str

class Word(BaseSchema):
    word: str
