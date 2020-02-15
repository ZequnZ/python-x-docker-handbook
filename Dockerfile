FROM python:3.8.1-slim

MAINTAINER ZequnZ "Zequn.zhou@n26.com"

WORKDIR  /app

COPY requirements.txt /app

RUN pip install --no-cache-dir -r requirements.txt

COPY ./src /app

EXPOSE 5000