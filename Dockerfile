FROM python:3.11
WORKDIR /app

COPY requirements.txt .
COPY Makefile .

RUN pip install -r requirements.txt

COPY . .

EXPOSE 8001

CMD ["make", "start"]
