# Layer 1: Base image with lightweight Python runtime
FROM python:3.12-slim

# Layer 2: Define working directory inside container
WORKDIR /app

# Layer 3: Copy requirement specifications
COPY requirements.txt .

# Layer 4: Copy application source code
COPY app.py .

# Layer 5: Expose application network port
EXPOSE 8080

# Layer 6: Entrypoint execution command
CMD ["python", "app.py"]
