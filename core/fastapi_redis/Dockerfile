FROM python:3.10.6-slim

WORKDIR  /app

COPY requirements/app.txt /app
COPY /src /app
RUN pip install --no-cache-dir -r app.txt 

ENTRYPOINT ["python", "-m", "main"]
