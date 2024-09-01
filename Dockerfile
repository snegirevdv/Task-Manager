FROM python:3.11
WORKDIR /app

RUN pip install gunicorn=20.1.0

COPY pyproject.toml .
COPY Makefile .

RUN pip install --no-cache-dir poetry
RUN poetry install

COPY . .

EXPOSE 8001

CMD ["make", "start"]
