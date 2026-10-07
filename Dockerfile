FROM python:3.12-slim

WORKDIR /app

COPY app.py login.py test_app.py ./

RUN python -m compileall .

EXPOSE 8080

CMD ["python", "-m", "http.server", "8080"]
