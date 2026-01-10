import random
from enum import Enum
from uuid import uuid4

import typer
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel


############
# entities #
############
def str_uuid() -> str:
    return str(uuid4())


class GameStatus(str, Enum):
    IN_PROGRESS = "in_progress"
    WON = "won"
    LOST = "lost"


class GameIsAlreadyOverError(Exception):
    ...


class Game:
    def __init__(
            self,
            max_errors: int,
            word_to_guess: str,
            id: str | None = None,
            errors: int = 0,
            selected_letters: list[str] | None = None,
    ):
        self._id = id or str_uuid()
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
        return "".join([l if l in self.selected_letters else "_" for l in self.word_to_guess])

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


#################
# words adapter #
#################
def get_random_word():
    words = []
    with open("words.txt", "r") as words_file:
        for word in words_file:
            words.append(word[:-1])
    return words[random.randint(0, len(words))]


##############
# games repo #
##############
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


################
# dependencies #
################
class Dependencies:
    games_repo = GamesRepo()


dependencies = Dependencies()


##########################
# use cases "controller" #
##########################
def init_game_use_case(
        max_errors: int,
        games_repo: GamesRepo = dependencies.games_repo,
) -> Game:
    game = Game(
        max_errors=max_errors,
        word_to_guess=get_random_word(),
    )
    games_repo.save(game=game)
    return game


def guess_letter_use_case(
        game_id: str,
        letter: str,
        games_repo: GamesRepo = dependencies.games_repo,
) -> Game:
    game = games_repo.get(game_id=game_id)
    game.add_selected_letter(letter=letter)
    games_repo.save(game=game)
    return game


###################
# adapter "views" #
###################

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


##################
# python adapter #
##################
def init_game(
        max_errors: int,
) -> GameModel:
    return GameModel.from_game(init_game_use_case(max_errors=max_errors))


def guess_letter(
        game_id: str,
        letter: str,
) -> GameModel:
    return GameModel.from_game(guess_letter_use_case(game_id=game_id, letter=letter))


###############
# api adapter #
###############
api = FastAPI()


class GameCreation(BaseModel):
    max_errors: int = 5


@api.post('/games')
def create_game(
        max_errors: int = 5,
) -> GameModel:
    return GameModel.from_game(init_game_use_case(max_errors=max_errors))


class Letter(BaseModel):
    letter: str


@api.post('/games/{game_id}/selected_letters')
def add_selected_letter(
        game_id: str,
        letter: Letter,
) -> GameModel:
    try:
        game = guess_letter_use_case(game_id=game_id, letter=letter.letter)
        return GameModel.from_game(game)
    except GameIsAlreadyOverError:
        raise HTTPException(status_code=400, detail="Game is already over")


###############
# cli client #
###############
app = typer.Typer()


@app.command()
def hangman(
        cheat_mode: bool = typer.Option(False, '--cheat', help="Activate cheat mode"),
        max_errors: int = typer.Option(5, '-e', help="Set the maximum number of errors allowed"),
):
    print("###################")
    print("Starting new game !")
    print("###################")

    # init game
    game = init_game(max_errors=max_errors)

    if cheat_mode:
        print('The word to guess is "' + game.word_to_guess + '" you cheater')

    while True:
        print("Your word so far is: " + game.word_so_far)

        letter = input("You have " + str(game.errors_left) + " errors left. Enter a letter: ")

        if 0 < len(letter) < 2:
            game = guess_letter(game_id=game.id, letter=letter)

            if game.game_status == GameStatus.WON:
                print("You won \o/")
                print("The word was " + game.word_to_guess)
                break
            elif game.game_status == GameStatus.LOST:
                print("You lost :(")
                print("The word was " + game.word_to_guess)
                break
        else:
            print("you didn't enter a letter")
