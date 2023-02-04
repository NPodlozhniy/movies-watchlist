import os
import pandas as pd

from aiogram import Bot, Dispatcher, executor, types

APP_TOKEN = os.environ.get("TOKEN")

PATH_TO_TABLE = "app/movies/movies_list.csv"

bot = Bot(token=APP_TOKEN)
dp = Dispatcher(bot)


def get_movies():
    return pd.read_csv(PATH_TO_TABLE)


@dp.message_handler(commands=["start", "list"])
async def all_movies(payload: types.Message):
    await payload.reply(f"```{get_movies().to_markdown(tablefmt='presto')}```", parse_mode="Markdown")


@dp.message_handler(commands="add")
async def add_movie(payload: types.Message):
    text = payload.get_args().strip()
    cur_movies = get_movies()
    if not text:
        message = f"Укажите название фильма"
    elif text in cur_movies.movie.values:
        message = f"Фильм *{text}* уже есть в списке"
    else:
        new_movie = pd.DataFrame({"movie": [text], "status": ["unwatched"]})
        updated_list = pd.concat([cur_movies, new_movie], ignore_index=True, axis=0)
        updated_list.to_csv(PATH_TO_TABLE, index=False)
        message = f"Фильм *{text}* добавлен"
    await payload.reply(message, parse_mode="Markdown")


@dp.message_handler(commands="watch")
async def watch_movie(payload: types.Message):
    text = payload.get_args().strip()
    df = get_movies()
    indexes = (df.movie == text)
    if sum(indexes) > 0:
        df.loc[df.movie == text, "status"] = "watched"
        df.to_csv(PATH_TO_TABLE, index=False)
        message = f"Фильм *{text}* просмотрен"
    else:
        message = f"Фильм *{text}* остутствует в списке"
    await payload.reply(message, parse_mode="Markdown")


if __name__ == "__main__":
    executor.start_polling(dp)
