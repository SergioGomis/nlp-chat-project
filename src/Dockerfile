FROM python:3.8.1-alpine3.11

COPY . /app

WORKDIR /app

RUN pip install -r requirements.txt

CMD ["python3","api.py"]