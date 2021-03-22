FROM python:3.8.1-slim

LABEL Author="ZequnZ" Link="https://github.com/ZequnZ/python-x-docker-handbook"

WORKDIR  /app

COPY requirements.txt /app
RUN pip install --no-cache-dir -r requirements.txt

ENTRYPOINT [ "jupyter-lab", "--ip=0.0.0.0", "--port=8999", "--no-browser", "--allow-root" ]
