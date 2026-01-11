from fastapi import FastAPI, HTTPException

from .models import GameNotFoundError, GameIsAlreadyOverError, WordAlreadyExists, WordNotFoundError, PlayerNotFoundError
from .views import GamePublic, PlayerPublic, PlayerEnum, GameCreation, Letter, Word
from .utils import init_game, guess_letter, add_word_to_repo, delete_word_from_repo, get_player, get_top_players

api = FastAPI()

@api.post('/games')
def create_game(
        GameCreation: GameCreation,
) -> GamePublic:
    return init_game(
        player_name=GameCreation.player_name,
        max_errors=GameCreation.max_errors,
        word_length=GameCreation.word_length,
    )

@api.post('/games/{game_id}/selected_letters')
def add_selected_letter(
        game_id: str,
        letter: Letter,
) -> GamePublic:
    try:
        return guess_letter(game_id=game_id, letter=letter.letter)
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
) -> PlayerPublic:
    try:
        return get_player(player_name=player_name)

    except PlayerNotFoundError:
        raise HTTPException(status_code=404, detail="Player not found")

@api.get('/top')
def get_top_players_endpoint(
    n: int = 10,
) -> list[PlayerEnum]:
    return get_top_players(n=n)
