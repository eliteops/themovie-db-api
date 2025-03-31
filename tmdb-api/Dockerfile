
FROM python:3.9


WORKDIR /tmdb-api


COPY ./requirements.txt /tmdb-api/requirements.txt


RUN pip install --no-cache-dir --upgrade -r /tmdb-api/requirements.txt


COPY ./app /tmdb-api/app

# COPY ./test_app /tmdb-api/test_app

# ENV PYTHONPATH=/tmdb-api

# RUN pytest -v

CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "80"]