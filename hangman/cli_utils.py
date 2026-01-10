import requests

from models import PlayerNotFoundError
from views import GamePublic, PlayerPublic, PlayerStats

SERVER_URL = "http://localhost:8000"

def request(method: str, endpoint: str, data: dict = None) -> dict:
    url = SERVER_URL + endpoint
    response = requests.request(method=method, url=url, json=data)
    response.raise_for_status()
    if response.status_code in (204, 201 ):
        return {}
    return response.json()

def init_game(
        player_name: str,
        max_errors: int,
) -> GamePublic:
    return GamePublic(**request(
        method="POST",
        endpoint="/games",
        data={
            "player_name": player_name,
            "max_errors": max_errors,
        },
    ))

def guess_letter(
        game_id: str,
        letter: str,
) -> GamePublic:
    return GamePublic(**request(
        method="POST",
        endpoint=f"/games/{game_id}/selected_letters",
        data={"letter": letter},
    ))

def add_word_to_repo(
        word: str,
) -> None:
    request(
        method="POST",
        endpoint="/words",
        data={"word": word},
    )

def delete_word_from_repo(
        word: str,
) -> None:
    request(
        method="DELETE",
        endpoint=f"/words/{word}",
    )

def get_player(
        player_name: str,
) -> PlayerPublic:
    try:
        return PlayerPublic(**request(
            method="GET",
            endpoint=f"/players/{player_name}",
        ))
    except requests.HTTPError as e:
        if e.response.status_code == 404:
            raise PlayerNotFoundError from e
        raise

def get_top_players(
        n: int = 10,
) -> list[PlayerStats]:
    players_data = request(
        method="GET",
        endpoint=f"/top?n={n}",
    )
    return [PlayerStats(**player_data) for player_data in players_data]