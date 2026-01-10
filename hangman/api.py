import uvicorn
from fastapi import FastAPI, HTTPException

from models import GameNotFoundError, GameIsAlreadyOverError, WordAlreadyExists, WordNotFoundError, PlayerNotFoundError
from views import GamePublic, PlayerPublic, GameCreation, Letter, Word
from utils import init_game, guess_letter, add_word_to_repo, delete_word_from_repo, get_player

api = FastAPI()

@api.post('/games')
def create_game(
        GameCreation: GameCreation,
) -> GamePublic:
    return GamePublic.from_game(init_game(
        max_errors=GameCreation.max_errors,
        player_name=GameCreation.player_name,
    ))


@api.post('/games/{game_id}/selected_letters')
def add_selected_letter(
        game_id: str,
        letter: Letter,
) -> GamePublic:
    try:
        game = guess_letter(game_id=game_id, letter=letter.letter)
        return GamePublic.from_game(game)
    except GameNotFoundError:
        raise HTTPException(status_code=404, detail="Game not found")
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

@api.delete('/words/{word}', status_code=204)
def delete_word(
    word: str,
) -> None:
    try:
        delete_word_from_repo(word=word)
    except WordNotFoundError:
        raise HTTPException(status_code=404, detail="Word not found")

@api.get('/players/{player_name}')
def get_player_endpoint(
    player_name: str,
):
    try:
        player = get_player(player_name=player_name)
        return PlayerPublic.from_player(player)

    except PlayerNotFoundError:
        raise HTTPException(status_code=404, detail="Player not found")


if __name__ == "__main__":
    uvicorn.run(api, host="0.0.0.0", port=8000)
