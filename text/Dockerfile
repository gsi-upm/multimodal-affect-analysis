FROM python:3.12-slim

LABEL org.opencontainers.image.source=https://github.com/gsi-upm/moral-values-detection

WORKDIR /app

COPY requirements.txt /app/
RUN pip install --no-cache-dir -r requirements.txt

COPY . /app/

EXPOSE 8000

CMD ["python", "server.py"]