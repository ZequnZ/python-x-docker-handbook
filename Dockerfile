FROM python:3.8.1-slim

LABEL Author="ZequnZ"
LABEL Email="zequn.zhou007@gmail.com"

WORKDIR  /app

COPY hello_world.py /app

CMD [ "python", "hello_world.py" ]
