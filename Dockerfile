FROM python:3.9.9
USER root
COPY ./producer/requirements.txt /requirements.txt

RUN python -m pip install -r /requirements.txt

COPY ./producer /app

WORKDIR /app