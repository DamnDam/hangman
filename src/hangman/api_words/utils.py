from ..repos import WordsRepo
from ..views import Word

################
# dependencies #
################
class Dependencies:
    words_repo = WordsRepo()

dependencies = Dependencies()


##########################
# use cases "controller" #
##########################

def get_random_word(
        word_length: int | None = None,
        words_repo: WordsRepo = dependencies.words_repo,
) -> Word:
    word_str = words_repo.get_random_word(word_length=word_length)
    return Word(word=word_str)

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
