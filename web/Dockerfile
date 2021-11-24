FROM python:slim

WORKDIR /usr/src/app

RUN apt update && apt install gcc -y
COPY requirements.txt requirements.txt
RUN python -m pip install -r requirements.txt

COPY  . .