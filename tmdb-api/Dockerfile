
FROM python:3.9


WORKDIR /tmdb-api


COPY ./requirements.txt /tmdb-api/requirements.txt


RUN pip install --no-cache-dir --upgrade -r /tmdb-api/requirements.txt


COPY ./app /tmdb-api/app


CMD ["fastapi", "run", "app/main.py", "--port", "80"]