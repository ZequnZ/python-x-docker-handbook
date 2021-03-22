FROM python:3.8.1-slim

LABEL Author="ZequnZ" Link="https://github.com/ZequnZ/python-x-docker-handbook"

WORKDIR  /app

COPY requirements.txt /app
RUN pip install --no-cache-dir -r requirements.txt
COPY ./src /app

CMD [ "-s", "43", "-l", "70" ]
ENTRYPOINT [ "python", "main.py" ]
