from models import Game, Player, GameStatus
from repo import GamesRepo, WordsRepo, PlayerRepo
from views import PlayerStats

################
# dependencies #
################
class Dependencies:
    games_repo = GamesRepo()
    words_repo = WordsRepo()
    player_repo = PlayerRepo(GamesRepo=games_repo)


dependencies = Dependencies()


##########################
# use cases "controller" #
##########################
def init_game(
        player_name: str,
        max_errors: int = 5,
        games_repo: GamesRepo = dependencies.games_repo,
        words_repo: WordsRepo = dependencies.words_repo,
) -> Game:
    game = Game(
        max_errors=max_errors,
        word_to_guess=words_repo.get_random_word(),
        player=Player(name=player_name),
    )
    games_repo.save(game=game)
    return game

def guess_letter(
        game_id: str,
        letter: str,
        games_repo: GamesRepo = dependencies.games_repo,
        player_repo: PlayerRepo = dependencies.player_repo,
) -> Game:
    game = games_repo.get(game_id=game_id)
    game.add_selected_letter(letter=letter)
    games_repo.save(game=game)
    if game.game_status != GameStatus.IN_PROGRESS:
        player_repo.save(player=game.player, game=game)
    return game

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
        player_repo: PlayerRepo = dependencies.player_repo,
) -> Player:
    return player_repo.get(player_name=player_name)

def get_top_players(
        n: int = 10,
        player_repo: PlayerRepo = dependencies.player_repo,
) -> list[PlayerStats]:
    return player_repo.get_top_players(n=n)