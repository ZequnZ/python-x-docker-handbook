FROM python:3.8.1-slim

LABEL Author="ZequnZ" Link="https://github.com/ZequnZ/python-x-docker-handbook"

WORKDIR  /app

COPY hello_world.py /app

CMD [ "python", "hello_world.py" ]
