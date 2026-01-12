from enum import Enum

class BaseModel:
    pass

class GameStatus(BaseModel, str, Enum):
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
    "BaseModel",
    "GameStatus",
    "GameNotFoundError",
    "GameIsAlreadyOverError",
    "WordNotFoundError",
    "WordAlreadyExists",
    "PlayerNotFoundError",
]