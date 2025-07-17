
FROM python:3.10-slim

WORKDIR /app


COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt


COPY chat.py .
COPY .env .


EXPOSE 7861


CMD ["python", "chat.py"]
