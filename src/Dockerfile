FROM python:3.10-slim

# copy files
WORKDIR /app 
COPY . .

RUN pip install -r requirements.txt

EXPOSE 8080 

# Entry point for the container
ENTRYPOINT ["uvicorn"]

# Default command to run Uvicorn
CMD ["app:app", "--host", "0.0.0.0", "--port", "8080", "--workers", "4", "--log-level", "info"]

