FROM python:3.10-slim

# copy files
WORKDIR /app 
COPY . .

RUN pip install -r requirements.txt

EXPOSE 8080 

uvicorn myapp:app --host 0.0.0.0 --port 8000 --workers 3 --log-level info

