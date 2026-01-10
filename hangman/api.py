import uvicorn
from fastapi import FastAPI, HTTPException

from models import GameIsAlreadyOverError, WordAlreadyExists
from views import GameModel, GameCreation, Letter, Word
from utils import init_game_use_case, guess_letter_use_case, add_word_to_repo

api = FastAPI()

@api.post('/games')
def create_game(
        GameCreation: GameCreation,
) -> GameModel:
    return GameModel.from_game(init_game_use_case(max_errors=GameCreation.max_errors))


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

@api.post('/words', status_code=201)
def add_word(
    word: Word,
) -> None:
    try:
        add_word_to_repo(word=word.word)
    except WordAlreadyExists:
        raise HTTPException(status_code=409, detail="Word already exists")


if __name__ == "__main__":
    uvicorn.run(api, host="0.0.0.0", port=8000)
