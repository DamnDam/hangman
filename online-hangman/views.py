from pydantic import BaseModel
from models import Game, GameStatus

class GameModel(BaseModel):
    id: str
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
            max_errors=game.max_errors,
            word_to_guess=game.word_to_guess,
            errors=game.errors,
            selected_letters=game.selected_letters,
            word_so_far=game.word_so_far,
            errors_left=game.errors_left,
            game_status=game.game_status,
        )
    
class GameCreation(BaseModel):
    max_errors: int = 5

class Letter(BaseModel):
    letter: str

