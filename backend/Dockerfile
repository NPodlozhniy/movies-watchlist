FROM python:3.7

WORKDIR /home

COPY requirements.txt requirements.txt

RUN pip install --upgrade pip && pip install --no-cache-dir -r requirements.txt

COPY app.py ./app/main.py

ENV PATH_TO_TABLE="app/movies/movies_list.csv"

ENTRYPOINT ["python", "./app/main.py"]