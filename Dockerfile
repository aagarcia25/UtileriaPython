# Dockerfile
FROM python:3.8-slim

WORKDIR /app

COPY requirements.txt .

RUN pip install --no-cache-dir -r requirements.txt

COPY . .

# Expone el puerto 93 para el tráfico web
EXPOSE 93

CMD ["python", "app.py"]

