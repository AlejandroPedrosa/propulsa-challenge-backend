# Backend Dockerfile
FROM python:3.9.10-alpine3.14
WORKDIR /app

COPY requirements.txt requirements.txt
RUN pip install --no-cache-dir -r requirements.txt
COPY . .

CMD ["python","app.py"]