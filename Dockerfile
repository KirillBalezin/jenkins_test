FROM python:3.11-slim-buster

WORKDIR /app

COPY . /app

# CMD ["python", "-m", "unittest", "discover", "-s", "tests"]
