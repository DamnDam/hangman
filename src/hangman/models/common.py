from enum import Enum

class GameStatus(str, Enum):
    IN_PROGRESS = "in_progress"
    WON = "won"
    LOST = "lost"

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

__all__ = [
    "GameStatus",
    "GameNotFoundError",
    "GameIsAlreadyOverError",
    "WordNotFoundError",
    "WordAlreadyExists",
    "PlayerNotFoundError",
]