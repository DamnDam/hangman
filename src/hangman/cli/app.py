import typer
import multiprocessing

from ..models import GameStatus, PlayerNotFoundError
from ..utils import uvicorn_serve

from . import services

app = typer.Typer()

@app.command()
def play(
        cheat_mode: bool = typer.Option(False, '--cheat', help="Activate cheat mode"),
        max_errors: int = typer.Option(0, '--max-errors', '-e', help="Set the maximum number of errors allowed"),
        word_length: int = typer.Option(0, '--word-length', '-l', help="Set the length of the word to guess"),
        player_name: str = typer.Option("", '--player', '-p', help="Set the player's name"),
        new_game: bool = typer.Option(False, '--new', '-n', help="Start a new game even if there are active games", is_flag=True),
        resume_game: str = typer.Option("", '--resume', '-r', help="Resume an active game by ID")
):
    print("###################")
    print("HANGMAN - RANKED !")
    print("####################\n")

    while not player_name:
        player_name = input("Enter your name: ")

    game = None
    try:
        player = services.get_player(player_name=player_name)
    except PlayerNotFoundError:
        print(f"Creating new player with name {player_name}")
    else:
        print("\n####################")
        print(f"Welcome back {player_name}!")
        print("Your stats:")
        print(f"Ranking: {player.ranking if player.ranking is not None else 'Unranked'}")
        print(f"Games won: {player.games_won}")
        print(f"Games lost: {player.games_lost}")
        print("####################\n")

        if resume_game:
            for iter_game in player.active_games:
                if iter_game.id == resume_game:
                    game = iter_game
                    print(f"Resuming game {game.id}...")
            if not game:
                print(f"No active game found with ID {resume_game}\n")
        if not game and not new_game and player.active_games:
            print("You have active games:")
            for i, iter_game in enumerate(player.active_games):
                print(
                    f"\t*{i+1} Game ID: {iter_game.id}, "
                    f"Word so far: {iter_game.word_so_far}, "
                    f"Errors left: {iter_game.errors_left}"
                )
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

    # init game
    if not game:
        game = services.init_game(
            player_name=player_name, 
            max_errors=max_errors if max_errors > 0 else None,
            word_length=word_length if word_length > 0 else None,
        )
        print(f"New game created with ID {game.id}")

    if cheat_mode:
        print(f'The word to guess is "{game.word_to_guess}" you cheater')
        print("Wait it does not work anymore...")

    while True:
        print("Your word so far is: " + game.word_so_far)

        letter = input("You have " + str(game.errors_left) + " errors left. Enter a letter: ")

        if 0 < len(letter) < 2:
            game = services.guess_letter(game_id=game.id, letter=letter)

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
def top(
        n: int = typer.Option(10, '--number', '-n', help="Number of top players to display"),
):
    top_players = services.get_top_players(n=n)
    print(f"Top {n} players:")
    for player in top_players:
        print(
            f"\t{player.name} - "
            f"Games Won: {player.games_won}, "
            f"Games Lost: {player.games_lost}, "
            f"Ranking: {player.ranking if player.ranking is not None else 'Unranked'}"
        )

@app.command()
def player(
        player_name: str = typer.Argument(..., help="The name of the player to retrieve"),
):
    try:
        player = services.get_player(player_name=player_name)
        print(f"Player: {player.name}")
        print(f"Ranking: {player.ranking if player.ranking is not None else 'Unranked'}")
        print(f"Games won: {player.games_won}")
        print(f"Games lost: {player.games_lost}")
    except PlayerNotFoundError:
        print(f"Player '{player_name}' not found")


words_app = typer.Typer()
app.add_typer(words_app, name="words")

@words_app.command("add")
def add_word(
        word: str = typer.Argument(..., help="The word to add to the repository"),
):
    try:
        services.add_word_to_repo(word=word)
        print(f'Word "{word}" added to the repository')
    except Exception as e:
            print(f"Error: {e}")

@words_app.command("delete")
def delete_word(
        word: str = typer.Argument(..., help="The word to delete from the repository"),
):
    try:
        services.delete_word_from_repo(word=word)
        print(f'Word "{word}" deleted from the repository')
    except Exception as e:
        print(f"Error: {e}")


serve_app = typer.Typer()
app.add_typer(serve_app, name="serve")

@serve_app.command("api")
def serve_api(
        host: str = typer.Option("localhost", help="Host to serve the API on"),
        port: int = typer.Option(8000, help="Port to serve the API on"),
):
    uvicorn_serve(
        module_name="api_main",
        host=host,
        port=port,
        service_name="MAIN",
    )

@serve_app.command("word")
def serve_word_api(
        host: str = typer.Option("localhost", help="Host to serve the Word API on"),
        port: int = typer.Option(8008, help="Port to serve the Word API on"),
):
    uvicorn_serve(
        module_name="api_words",
        host=host,
        port=port,
        service_name="WORD",
    )

@serve_app.callback(invoke_without_command=True)
def serve_callback(
        ctx: typer.Context,
        port: int = typer.Option(8000, help="Port to serve the API on"),
        word_port: int = typer.Option(8008, help="Port to serve the Word API on"),
        host: str = typer.Option("localhost", help="Host to serve the APIs on"),
):
    """Serve the Hangman application with all required components."""
    if not ctx.invoked_subcommand is None:
        return
    
    word_api_process = multiprocessing.Process(
        target=serve_word_api,
        kwargs={"host": host, "port": word_port},
    )
    word_api_process.start()

    try:
        serve_api(host=host, port=port)
    finally:
        word_api_process.terminate()
        word_api_process.join()