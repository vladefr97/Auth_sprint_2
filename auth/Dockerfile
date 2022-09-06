FROM python:3.9.7-buster

COPY requirements.txt .

RUN pip3 install -r requirements.txt --no-cache-dir

COPY src .

COPY utils .
