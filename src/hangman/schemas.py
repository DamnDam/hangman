from pydantic import RootModel, BaseModel as PydanticBaseModel

from .models import BaseModel, Game, GameStatus, Player

class BaseSchema(PydanticBaseModel):
    _BaseModel: type[BaseModel]

    @staticmethod
    def from_model(model: BaseModel, *args, **kwargs) -> 'BaseSchema':
        raise NotImplementedError()

    class Config:
        extra = 'allow'

class PlayerBase(BaseSchema):
    _BaseModel = Player
    name: str

class PlayerModel(PlayerBase):
    games_won: int
    games_lost: int
    ranking: int | None = None

    @staticmethod
    def from_model(model: 'Player') -> 'PlayerModel':
        return PlayerModel(
            name=model.name,
            games_won=model.total_wins,
            games_lost=model.total_losses,
            ranking=model.ranking,
        )

class PlayerEnum(PlayerModel):
    pass

class PlayerList(RootModel):
    root: list[PlayerEnum]

class PlayerPublic(PlayerEnum):
    active_games: list["GameEnum"]

    @staticmethod
    def from_model(model: 'Player', active_games: list[Game]) -> 'PlayerPublic':
        return PlayerPublic(
            name=model.name,
            games_won=model.total_wins,
            games_lost=model.total_losses,
            ranking=model.ranking,
            active_games=[GameEnum.from_model(game) for game in active_games],
        )

class GameCreation(BaseSchema):
    _BaseModel = Game
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
    def from_model(model: Game) -> 'GameModel':
        return GameModel(
            id=model.id,
            player_name=model.player.name,
            max_errors=model.max_errors,
            word_to_guess=model.word_to_guess,
            errors=model.errors,
            selected_letters=model.selected_letters,
            word_so_far=model.word_so_far,
            errors_left=model.errors_left,
            game_status=model.game_status,
        )

class GameEnum(GameBase):
    @staticmethod
    def from_model(model: Game) -> 'GamePublic':
        return GamePublic(
            id=model.id,
            player_name=model.player.name,
            max_errors=model.max_errors,
            word_so_far=model.word_so_far,
            word_to_guess=model.word_to_guess if model.game_status != GameStatus.IN_PROGRESS else None,
            errors_left=model.errors_left,
            game_status=model.game_status,
        )

class GameList(RootModel):
    root: list[GameEnum]

class GamePublic(GameEnum):
    pass

class Letter(BaseSchema):
    letter: str

class Word(BaseSchema):
    word: str

class WordList(RootModel):
    root: list[Word]