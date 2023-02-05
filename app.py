import os
import logging

import pandas as pd
from aiogram import Bot, Dispatcher, executor, types

logging.basicConfig(
    format="%(levelname)s : %(asctime)s - %(message)s",
    datefmt="%d-%b-%y %H:%M:%S",
    level=logging.INFO,
)

APP_TOKEN = os.environ.get("TOKEN")
PATH_TO_TABLE = os.environ.get("PATH_TO_TABLE")

bot = Bot(token=APP_TOKEN)
dp = Dispatcher(bot)


def formatter(name: str) -> str:
    return ' '.join([
        x[0].upper() + x[1:].lower() if len(x) > 3 else x.lower()
        for x in name.strip().split(' ')
    ])


def get_movies():
    return pd.read_csv(PATH_TO_TABLE)


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
        new_movie = pd.DataFrame({"movie": [text], "status": ["unwatched"]})
        updated_list = pd.concat([cur_movies, new_movie], ignore_index=True, axis=0)
        updated_list.to_csv(PATH_TO_TABLE, index=False)
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
        cur_movies.loc[indexes, "status"] = "watched"
        cur_movies.to_csv(PATH_TO_TABLE, index=False)
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
        cur_movies[-indexes].to_csv(PATH_TO_TABLE, index=False)
        message = f"Фильм *{text}* удален"
    logging.info(message)
    await payload.reply(message, parse_mode="Markdown")


if __name__ == "__main__":
    executor.start_polling(dp)
