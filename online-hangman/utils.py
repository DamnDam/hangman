import random

from models import Game
from repo import GamesRepo
from views import GameModel

#################
# words adapter #
#################
def get_random_word():
    words = []
    with open("words.txt", "r") as words_file:
        for word in words_file:
            words.append(word[:-1])
    return words[random.randint(0, len(words))]


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
