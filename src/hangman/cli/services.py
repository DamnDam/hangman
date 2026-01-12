from requests import HTTPError

from ..models import PlayerNotFoundError
from ..schemas import GamePublic, PlayerPublic, PlayerEnum
from ..utils import request_factory

MAIN_API_URL = "http://localhost:8000"
WORD_API_URL = "http://localhost:8008"

################
# dependencies #
################
class Dependencies:
    main_request = staticmethod(request_factory(server_url=MAIN_API_URL))
    word_request = staticmethod(request_factory(server_url=WORD_API_URL))


dependencies = Dependencies()


##########################
# use cases "controller" #
##########################

def init_game(
        player_name: str,
        max_errors: int | None = None,
        word_length: int | None = None,
        request = dependencies.main_request,
) -> GamePublic:
    data={
        "player_name": player_name,
    }
    if max_errors:
        data["max_errors"] = max_errors
    if word_length:
        data["word_length"] = word_length
    return GamePublic.model_validate_json(request(
        method="POST",
        endpoint="/games",
        data=data,
    ))

def guess_letter(
        game_id: str,
        letter: str,
        request = dependencies.main_request,
) -> GamePublic:
    return GamePublic.model_validate_json(request(
        method="POST",
        endpoint=f"/games/{game_id}/selected_letters",
        data={"letter": letter},
    ))

def get_player(
        player_name: str,
        request = dependencies.main_request,
) -> PlayerPublic:
    print("Getting player:", player_name)
    try:
        return PlayerPublic.model_validate_json(request(
            method="GET",
            endpoint=f"/players/{player_name}",
        ))
    except HTTPError as e:
        if e.response.status_code == 404:
            raise PlayerNotFoundError from e
        raise

def get_top_players(
        n: int = 10,
        request = dependencies.main_request,
) -> list[PlayerEnum]:
    players_data = request(
        method="GET",
        endpoint=f"/top?n={n}",
    )
    return [PlayerEnum.model_validate_json(player_data) for player_data in players_data]

def add_word_to_repo(
        word: str,
        request = dependencies.word_request,
) -> None:
    request(
        method="POST",
        endpoint="/words",
        data={"word": word},
    )

def delete_word_from_repo(
        word: str,
        request = dependencies.word_request,
) -> None:
    request(
        method="DELETE",
        endpoint=f"/words/{word}",
    )

__all__ = [
    "init_game",
    "guess_letter",
    "get_player",
    "get_top_players",
    "add_word_to_repo",
    "delete_word_from_repo",
]