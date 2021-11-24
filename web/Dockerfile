FROM python:slim

WORKDIR /usr/src/app

RUN apt update && apt install gcc -y
ENV TZ=Europe/Berlin
RUN ln -snf /usr/share/zoneinfo/$TZ /etc/localtime && echo $TZ > /etc/timezone
COPY requirements.txt requirements.txt
RUN python -m pip install -r requirements.txt

COPY  . .