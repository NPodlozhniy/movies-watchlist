import os
import logging

import psycopg2
import pandas as pd
from aiogram import Bot, Dispatcher, executor, types

logging.basicConfig(
    format="%(levelname)s : %(asctime)s - %(message)s",
    datefmt="%d-%b-%y %H:%M:%S",
    level=logging.INFO,
)

APP_TOKEN = os.environ.get("TOKEN")

bot = Bot(token=APP_TOKEN)
dp = Dispatcher(bot)


def database_connection():
    return psycopg2.connect(
        host = os.environ.get("HOST", "localhost"),
        user = "postgres",
        password = "qwerty",
        port = "5432",
        database = "movies_db",
    )


def dml(statement: str):
    try:
        conn = database_connection()
        cur = conn.cursor()
        cur.execute(statement)
        conn.commit()
        cur.close()
        conn.close()
    except psycopg2.DatabaseError as error:
        return f"{error}", 500


def formatter(name: str) -> str:
    return ' '.join([
        x[0].upper() + x[1:].lower() if len(x) > 3 else x.lower()
        for x in name.strip().split(' ')
    ])


def get_movies():
    try:
        conn = database_connection()
        cur = conn.cursor()
        cur.execute("SELECT movie, status FROM movies_table")
        data = cur.fetchall()
        cur.close()
        conn.close()
        cur.close()
        conn.close()
        return pd.DataFrame(data, columns=["movie", "status"])
    except psycopg2.DatabaseError as error:
        return f"{error}", 500


@dp.message_handler(commands=["start", "list"])
async def all_movies(payload: types.Message):
    df = get_movies()
    df['№'] = df.index + 1
    await payload.reply(f"```{df.set_index('№').to_markdown(tablefmt='grid')}```", parse_mode="Markdown")


@dp.message_handler(commands="add")
async def add_movie(payload: types.Message):
    text = formatter(payload.get_args())
    cur_movies = get_movies()
    if not text:
        message = f"Необходимо указать название фильма"
    elif text in cur_movies.movie.values:
        message = f"Фильм *{text}* уже есть в списке"
    else:
        dml(f"INSERT INTO movies_table (movie, status) VALUES ('{text}', 'unwatched')")
        message = f"Фильм *{text}* добавлен"
    logging.info(message)
    await payload.reply(message, parse_mode="Markdown")


@dp.message_handler(commands="watch")
async def watch_movie(payload: types.Message):
    text = formatter(payload.get_args())
    cur_movies = get_movies()
    indexes = (cur_movies.movie == text)
    if sum(indexes) == 0:
        message = f"Сперва фильм *{text}* надо добавить в список"
    else:
        dml(f"UPDATE movies_table SET status = 'watched' WHERE movie = '{text}'")
        message = f"Фильм *{text}* просмотрен"
    logging.info(message)
    await payload.reply(message, parse_mode="Markdown")


@dp.message_handler(commands="del")
async def del_movie(payload: types.Message):
    text = formatter(payload.get_args())
    cur_movies = get_movies()
    indexes = (cur_movies.movie == text)
    if sum(indexes) == 0:
        message = f"Фильм *{text}* и так остутствует в списке"
    else:
        dml(f"DELETE FROM movies_table WHERE movie = '{text}'")
        message = f"Фильм *{text}* удален"
    logging.info(message)
    await payload.reply(message, parse_mode="Markdown")


if __name__ == "__main__":
    executor.start_polling(dp)
