import requests

from views import GameModel

SERVER_URL = "http://localhost:8000"

def request(method: str, endpoint: str, data: dict = None) -> dict:
    url = SERVER_URL + endpoint
    response = requests.request(method=method, url=url, json=data)
    response.raise_for_status()
    return response.json()

def init_game(
        max_errors: int,
) -> GameModel:
    return GameModel(**request(
        method="POST",
        endpoint="/games",
        data={"max_errors": max_errors},
    ))

def guess_letter(
        game_id: str,
        letter: str,
) -> GameModel:
    return GameModel(**request(
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