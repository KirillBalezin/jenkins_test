FROM python:3.11-slim-buster

WORKDIR /app

COPY calc.py /app/
COPY tests /app/tests/
