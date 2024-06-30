FROM python:3.9-slim

WORKDIR /app

COPY . .

RUN pip install -r requirements.txt

EXPOSE 3000
EXPOSE 5000

CMD ["python", "main.py", "0.0.0.0"]
