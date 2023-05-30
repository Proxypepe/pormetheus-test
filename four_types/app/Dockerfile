FROM python:3.12.0a3-alpine3.17

WORKDIR /app

COPY app.py requirements.txt .

RUN pip install -r requirements.txt

EXPOSE 8080

CMD ["gunicorn"  , "--bind", "0.0.0.0:8080", "app:app", "-k", "uvicorn.workers.UvicornWorker"]
