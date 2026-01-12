from fastapi import FastAPI, Depends, HTTPException

from ..models import GameNotFoundError, GameIsAlreadyOverError, PlayerNotFoundError
from ..schemas import GamePublic, PlayerPublic, PlayerEnum, GameCreation, Letter

from . import services

app = FastAPI()

@app.post('/games')
def create_game(
        game_creation: GameCreation,
) -> GamePublic:
    return services.init_game(
        player_name=game_creation.player_name,
        max_errors=game_creation.max_errors,
        word_length=game_creation.word_length,
    )

@app.post('/games/{game_id}/selected_letters')
def add_selected_letter(
        game_id: str,
        letter: Letter,
) -> GamePublic:
    try:
        return services.guess_letter(game_id=game_id, letter=letter.letter)
    except GameNotFoundError:
        raise HTTPException(status_code=404, detail="Game not found")
    except GameIsAlreadyOverError:
        raise HTTPException(status_code=400, detail="Game is already over")

@app.get('/players/{player_name}')
def get_player_endpoint(
        player_name: str,
) -> PlayerPublic:
    try:
        return services.get_player(player_name=player_name)

    except PlayerNotFoundError:
        raise HTTPException(status_code=404, detail="Player not found")

@app.get('/top')
def get_top_players_endpoint(
        n: int = 10,
) -> list[PlayerEnum]:
    return services.get_top_players(n=n)