import typer

from cli_utils import init_game, guess_letter, add_word_to_repo
from models import GameStatus

app = typer.Typer()

@app.command()
def hangman(
        cheat_mode: bool = typer.Option(False, '--cheat', help="Activate cheat mode"),
        max_errors: int = typer.Option(5, '-e', help="Set the maximum number of errors allowed"),
):
    print("###################")
    print("Starting new game !")
    print("###################")

    # init game
    game = init_game(max_errors=max_errors)

    if cheat_mode:
        print('The word to guess is "' + game.word_to_guess + '" you cheater')

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
def add_word(
        word: str = typer.Argument(..., help="The word to add to the repository"),
):
    try:
        add_word_to_repo(word=word)
        print(f'Word "{word}" added to the repository')
    except Exception as e:
        print(f"Error: {e}")

if __name__ == "__main__":
    app()