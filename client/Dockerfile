FROM python:3.13.7-slim

RUN apt update && apt install -y postgresql-contrib

COPY ./requirements.txt /requirements.txt
RUN pip install --no-cache-dir -r /requirements.txt

COPY . /app
WORKDIR /app

ENTRYPOINT [ "python", "main.py" ]