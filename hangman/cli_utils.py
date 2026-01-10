import requests

from views import GamePublic

SERVER_URL = "http://localhost:8000"

def request(method: str, endpoint: str, data: dict = None) -> dict:
    url = SERVER_URL + endpoint
    response = requests.request(method=method, url=url, json=data)
    response.raise_for_status()
    if response.status_code in (204, 201 ):
        return {}
    return response.json()

def init_game(
        max_errors: int,
) -> GamePublic:
    return GamePublic(**request(
        method="POST",
        endpoint="/games",
        data={"max_errors": max_errors},
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