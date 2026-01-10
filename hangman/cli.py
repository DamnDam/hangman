import typer

from cli_utils import init_game, guess_letter, add_word_to_repo, delete_word_from_repo, get_player
from models import GameStatus, PlayerNotFoundError

app = typer.Typer()

@app.command()
def hangman(
        cheat_mode: bool = typer.Option(False, '--cheat', help="Activate cheat mode"),
        max_errors: int = typer.Option(5, '-e', help="Set the maximum number of errors allowed"),
        player_name: str = typer.Option("", '--player', '-p', help="Set the player's name"),
):
    print("###################")
    print("HANGMAN - RANKED !")
    print("###################")

    while not player_name:
        player_name = input("Enter your name: ")

    game = None
    try:
        player = get_player(player_name=player_name)
        print(f"Welcome back {player_name}!")

        print("Your stats:")
        print(f"Ranking: {player.ranking if player.ranking is not None else 'Unranked'}")
        print(f"Total games: {player.total_games}")
        print(f"Games won: {player.games_won}")
        print(f"Games lost: {player.games_lost}")

        if player.active_games:
            print("You have active games:")
            for i, iter_game in enumerate(player.active_games):
                print(f"\t*{i+1} Game ID: {iter_game.id}, Word so far: {iter_game.word_so_far}, Errors left: {iter_game.errors_left}")
            resume = ""
            while not resume.lower() in ['y', 'n']:
                resume = input("Do you want to resume an active game? (y/n): ")
            if resume.lower() == 'y':
                game_index = -1
                while game_index < 0 or game_index >= len(player.active_games):
                    try:
                        game_index = int(input("Enter the number of the game you want to resume: ")) - 1
                    except ValueError:
                        game_index = -1
                game = player.active_games[game_index]
                print(f"Resuming game {game.id}...")
                
    except PlayerNotFoundError:
        print(f"Creating new player with name {player_name}")

    # init game
    if not game:
        game = init_game(player_name=player_name, max_errors=max_errors)
        print(f"New game created with ID {game.id}")

    if cheat_mode:
        print(f'The word to guess is "{game.word_to_guess}" you cheater')
        print("Wait it does not work anymore...")

    while True:
        print("Your word so far is: " + game.word_so_far)

        letter = input("You have " + str(game.errors_left) + " errors left. Enter a letter: ")

        if 0 < len(letter) < 2:
            game = guess_letter(game_id=game.id, letter=letter)

            if game.game_status == GameStatus.WON:
                print("You won \\o/")
                print("The word was " + game.word_to_guess)
                break
            elif game.game_status == GameStatus.LOST:
                print("You lost :(")
                print("The word was " + game.word_to_guess)
                break
        else:
            print("you didn't enter a letter")

@app.command()
def words(
    word: str = typer.Argument(..., help="The word to add to the repository"),
    add: bool = typer.Option(False, '--add', '-a', help="Add a word to the repository", is_flag=True),
    delete: bool = typer.Option(False, '--delete', '-d', help="Delete a word from the repository", is_flag=True),
):
    if add:
        try:
            add_word_to_repo(word=word)
            print(f'Word "{word}" added to the repository')
        except Exception as e:
            print(f"Error: {e}")
    elif delete:
        try:
            delete_word_from_repo(word=word)
            print(f'Word "{word}" deleted from the repository')
        except Exception as e:
            print(f"Error: {e}")
    else:
        print("You must specify either --add or --delete")

@app.command()
def top(
    n: int = typer.Option(10, '--number', '-n', help="Number of top players to display"),
):
    from cli_utils import get_top_players
    top_players = get_top_players(n=n)
    print(f"Top {n} players:")
    for player in top_players:
        print(f"\t{player.name} - Games Won: {player.games_won}, Games Lost: {player.games_lost}, Ranking: {player.ranking if player.ranking is not None else 'Unranked'}")

@app.command()
def player(
    player_name: str = typer.Argument(..., help="The name of the player to retrieve"),
):
    try:
        player = get_player(player_name=player_name)
        print(f"Player: {player.name}")
        print(f"Ranking: {player.ranking if player.ranking is not None else 'Unranked'}")
        print(f"Total games: {player.total_games}")
        print(f"Games won: {player.games_won}")
        print(f"Games lost: {player.games_lost}")
    except PlayerNotFoundError:
        print(f"Player '{player_name}' not found")

if __name__ == "__main__":
    app()