FROM python:3.12.5-slim-bookworm

ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

WORKDIR /app

COPY requirements.txt requirements.txt

RUN pip install -r requirements.txt

COPY . .

CMD ["/bin/sh", "-c", "flask db upgrade && flask run --host=0.0.0.0"]