from enum import Enum
from uuid import uuid4
from pydantic import BaseModel

def str_uuid() -> str:
    return str(uuid4())

class GameNotFoundError(Exception):
    ...

class GameIsAlreadyOverError(Exception):
    ...

class WordNotFoundError(Exception):
    ...

class WordAlreadyExists(Exception):
    ...

class PlayerNotFoundError(Exception):
    ...

class Player:
    def __init__(
            self,
            name: str,
            games: list["Game"] | None = None,
            total_wins: int = 0,
            total_losses: int = 0,
            ranking: int | None = None,
    ):
        self._name = name
        self._games = games or []
        self._total_wins = total_wins
        self._total_losses = total_losses
        self._ranking = ranking

    @property
    def id(self) -> str:
        return self._id

    @property
    def name(self) -> str:
        return self._name
    
    @property
    def games(self) -> list["Game"]:
        return self._games
    
    @property
    def total_wins(self) -> int:
        return self._total_wins
    
    @property
    def total_losses(self) -> int:
        return self._total_losses
    
    @property
    def ranking(self) -> int | None:
        return self._ranking
    
    def update_score(self, game: "Game") -> None:
        if game.game_status == GameStatus.WON:
            self._total_wins += 1
        elif game.game_status == GameStatus.LOST:
            self._total_losses += 1

class GameStatus(str, Enum):
    IN_PROGRESS = "in_progress"
    WON = "won"
    LOST = "lost"

class Game:
    def __init__(
            self,
            max_errors: int,
            word_to_guess: str,
            player: "Player",
            id: str | None = None,
            errors: int = 0,
            selected_letters: list[str] | None = None,
    ):
        self._id = id or str_uuid()
        self._player = player
        self._max_errors = max_errors
        self._word_to_guess = word_to_guess
        self._errors = errors
        self._selected_letters = selected_letters or []

    @property
    def selected_letters(self) -> list[str]:
        return self._selected_letters

    @property
    def word_to_guess(self) -> str:
        return self._word_to_guess

    @property
    def player(self) -> "Player":
        return self._player

    @property
    def errors(self) -> int:
        return self._errors

    @property
    def id(self) -> str:
        return self._id

    @property
    def max_errors(self) -> int:
        return self._max_errors

    @property
    def word_so_far(self) -> str:
        return "".join([l if l in self.selected_letters else "-" for l in self.word_to_guess])

    @property
    def errors_left(self) -> int:
        return self.max_errors - self.errors

    @property
    def game_status(self) -> GameStatus:
        if self.max_errors == self.errors:
            return GameStatus.LOST
        elif self.word_so_far == self.word_to_guess:
            return GameStatus.WON
        else:
            return GameStatus.IN_PROGRESS

    def add_selected_letter(self, letter: str) -> None:
        if self.game_status != GameStatus.IN_PROGRESS:
            raise GameIsAlreadyOverError()
        self.selected_letters.append(letter)
        if letter not in self.word_to_guess:
            self._errors += 1