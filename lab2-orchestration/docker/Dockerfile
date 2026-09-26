# Base image
FROM python:3.11-slim

# Set working directory
WORKDIR /app

# Set environment variables for unbuffered output
ENV PYTHONUNBUFFERED=1

# Copy original application files
COPY app.py .
COPY login.py .

# Copy orchestration runner
COPY lab2-orchestration/docker/entrypoint.py .

# Run entrypoint
CMD ["python", "-u", "entrypoint.py"]
