FROM python:slim

WORKDIR /usr/src/app

COPY requirements.txt requirements.txt
RUN python -m pip install -r requirements.txt

COPY  . .