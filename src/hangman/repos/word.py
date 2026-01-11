import random

from .base import BaseRepo
from ..models import WordAlreadyExists, WordNotFoundError

class WordsRepo(BaseRepo):
    _repo: dict[str, list[str]]

    _filename = "data/words.txt"
    _default_provided = True

    def _reload(self):
        with open(self._filename, "r") as words_file:
            word_list = words_file.readlines()
        # Group words by their length
        self._repo = {}
        for word in word_list:
            clean_word = word.strip()
            key = str(len(clean_word))
            self._repo.setdefault(key, []).append(clean_word)
    
    def _persist(self):
        with open(self._filename, "w") as words_file:
            for word_list in self._repo.values():
                for word in word_list:
                    words_file.write(word + "\n")

    def get_random_word(self, word_length: int | None = None) -> str:
        words_list = self.get_words_list(word_length=word_length)
        if not words_list:
            raise WordNotFoundError()
        return random.choice(words_list)

    def get_words_list(self, word_length: int | None = None) -> list[str]:
        if word_length is not None:
            return self._repo.get(str(word_length), [])
        return [word for words_list in self._repo.values() for word in words_list]

    def add_word(self, word: str):
        clean_word = word.strip()
        key = str(len(clean_word))
        if clean_word in self._repo.get(key, []):
            raise WordAlreadyExists()
        self._repo.setdefault(key, []).append(clean_word)
        self._persist()
    
    def delete_word(self, word: str):
        clean_word = word.strip()
        key = str(len(clean_word))
        if clean_word not in self._repo.get(key, []):
            raise WordNotFoundError()
        self._repo[key].remove(clean_word)
        self._persist()