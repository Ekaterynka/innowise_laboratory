# Use Python slim image for smaller size
FROM python:3.11-slim

# Set working directory inside container
WORKDIR /app

# Copy and install dependencies
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy application code
COPY . .

# Expose FastAPI port 8000
EXPOSE 8000

# Set environment variables
ENV HOST=0.0.0.0 PORT=8000

# Start FastAPI application
CMD ["sh", "-c", "uvicorn main:app --host ${HOST} --port ${PORT}"]