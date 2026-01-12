from fastapi import FastAPI, HTTPException

from ..models import WordAlreadyExists, WordNotFoundError
from ..schemas import Word

from .services import *

app = FastAPI()

@app.get('/word')
def get_word(
        word_length: int | None = None,
) -> Word:
    try:
        return get_random_word(word_length=word_length)
    except WordNotFoundError:
        raise HTTPException(status_code=404, detail="No word found with the specified length")
    
@app.post('/words', status_code=201)
def add_word(
        word: Word,
) -> None:
    try:
        add_word_to_repo(word=word.word)
    except WordAlreadyExists:
        raise HTTPException(status_code=409, detail="Word already exists")

@app.delete('/words/{word}', status_code=204)
def delete_word(
        word: str,
) -> None:
    try:
        delete_word_from_repo(word=word)
    except WordNotFoundError:
        raise HTTPException(status_code=404, detail="Word not found")
