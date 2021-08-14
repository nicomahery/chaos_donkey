FROM python:3.9.6-slim

WORKDIR /src

COPY requirements.txt .

RUN pip install -r requirements.txt

COPY main.py .
COPY fonts/ ./fonts

CMD ["python", "./main.py"]