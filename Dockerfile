# syntax=docker/dockerfile:1

FROM python:3.8-slim-buster

WORKDIR /issconv

COPY requirements.txt requirements.txt
RUN pip3 install -r requirements.txt

COPY . .
EXPOSE 8080
CMD [ "waitress-serve", "--call" , "app:run"]