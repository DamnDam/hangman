import uvicorn
from fastapi import FastAPI, HTTPException

from models import GameIsAlreadyOverError
from views import GameModel, Letter
from utils import init_game_use_case, guess_letter_use_case

api = FastAPI()

@api.post('/games')
def create_game(
        max_errors: int = 5,
) -> GameModel:
    return GameModel.from_game(init_game_use_case(max_errors=max_errors))


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

if __name__ == "__main__":
    uvicorn.run(api, host="0.0.0.0", port=8000)
