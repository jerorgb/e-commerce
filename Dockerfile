FROM python:3.11-slim

WORKDIR /app

COPY requirements.txt ./
RUN pip install --no-cache-dir -r requirements.txt

COPY . .

EXPOSE 8000

CMD ["uvicorn", "src.infrastructure.api.main:app", "--host", "localhost", "--port", "8000", "/docs#"]
##http://localhost:8000/docs#/