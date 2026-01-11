from ..models import Game, GameStatus
from ..repos import GamesRepo, WordsRepo, PlayersRepo
from ..views import GamePublic, PlayerPublic, PlayerEnum

################
# dependencies #
################
class Dependencies:
    words_repo = WordsRepo()
    player_repo = PlayersRepo()
    games_repo = GamesRepo(player_repo=player_repo)

dependencies = Dependencies()


##########################
# use cases "controller" #
##########################
def init_game(
        player_name: str,
        max_errors: int,
        word_length: int | None = None,
        games_repo: GamesRepo = dependencies.games_repo,
        words_repo: WordsRepo = dependencies.words_repo,
        player_repo: PlayersRepo = dependencies.player_repo,
) -> GamePublic:
    player = player_repo.get(player_name=player_name, nofail=True)
    game = Game(
        max_errors=max_errors,
        word_to_guess=words_repo.get_random_word(word_length=word_length),
        player=player,
    )
    games_repo.save(game=game)
    return GamePublic.from_game(game=game)

def guess_letter(
        game_id: str,
        letter: str,
        games_repo: GamesRepo = dependencies.games_repo,
        player_repo: PlayersRepo = dependencies.player_repo,
) -> GamePublic:
    game = games_repo.get(game_id=game_id)
    game.add_selected_letter(letter=letter)
    games_repo.save(game=game)
    if game.game_status != GameStatus.IN_PROGRESS:
        # Game is over, update player stats
        player_repo.save_result(player=game.player, game_status=game.game_status)
    return GamePublic.from_game(game=game)

def add_word_to_repo(
        word: str,
        words_repo: WordsRepo = dependencies.words_repo,
):
    words_repo.add_word(word=word)

def delete_word_from_repo(
        word: str,
        words_repo: WordsRepo = dependencies.words_repo,
):
    words_repo.delete_word(word=word)

def get_player(
        player_name: str,
        player_repo: PlayersRepo = dependencies.player_repo,
        games_repo: GamesRepo = dependencies.games_repo,
) -> PlayerPublic:
    player = player_repo.get(player_name=player_name)
    active_games = [
        game 
        for game in games_repo.list_for_player(player_name=player_name) 
        if game.game_status == GameStatus.IN_PROGRESS
    ]
    return PlayerPublic.from_player(player=player, active_games=active_games)

def get_top_players(
        n: int = 10,
        player_repo: PlayersRepo = dependencies.player_repo,
) -> list[PlayerEnum]:
    return player_repo.get_top_players(n=n)