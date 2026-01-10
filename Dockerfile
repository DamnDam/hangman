FROM python:3.13

RUN mkdir /app
WORKDIR /app

COPY requirements.txt .

RUN pip install -r requirements.txt

ADD ./hangman /app/hangman

COPY words.txt .

CMD ["python", "hangman/cli.py"]