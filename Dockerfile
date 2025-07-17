# Use official Python image as base
FROM python:3.10-slim

# Set working directory
WORKDIR /app

# Copy requirements and install dependencies
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy the rest of the application code
COPY chat.py .
COPY .env .

# Expose the port the app runs on
EXPOSE 7861

# Command to run the app
CMD ["python", "chat.py"]
