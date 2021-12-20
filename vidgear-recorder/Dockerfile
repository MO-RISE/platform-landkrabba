FROM python:3.9-slim

RUN apt update && apt install -y ffmpeg

COPY requirements.txt requirements.txt

RUN pip3 install -r requirements.txt

WORKDIR /app

COPY main.py main.py

CMD ["python3", "main.py"]