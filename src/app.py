import logging
import os
import random
import time
from typing import Optional

import httpx
import uvicorn
from fastapi import FastAPI, Response
from utils import PrometheusMiddleware, metrics  # Import the metrics utilities

APP_NAME = os.environ.get("APP_NAME", "app")
EXPOSE_PORT = os.environ.get("EXPOSE_PORT", 8000)

app = FastAPI()

# Setting metrics middleware for Prometheus
app.add_middleware(PrometheusMiddleware, app_name=APP_NAME)
app.add_route("/metrics", metrics)


class EndpointFilter(logging.Filter):
    # Uvicorn endpoint access log filter
    def filter(self, record: logging.LogRecord) -> bool:
        return record.getMessage().find("GET /metrics") == -1


# Filter out /metrics endpoint from the logs
logging.getLogger("uvicorn.access").addFilter(EndpointFilter())

# Log configuration (for Promtail)
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s %(levelname)s [%(name)s] [%(filename)s:%(lineno)d] - %(message)s',
    handlers=[logging.StreamHandler()]  # Output logs to stdout for Promtail
)


@app.get("/")
async def read_root():
    logging.info("Hello World")
    return {"Hello": "World"}


@app.get("/items/{item_id}")
async def read_item(item_id: int, q: Optional[str] = None):
    logging.info("Accessed /items endpoint")
    return {"item_id": item_id, "q": q}


@app.get("/io_task")
async def io_task():
    time.sleep(1)
    logging.info("IO bound task finished")
    return "IO bound task finished!"


@app.get("/cpu_task")
async def cpu_task():
    for i in range(1000):
        _ = i * i * i
    logging.info("CPU bound task finished")
    return "CPU bound task finished!"


@app.get("/random_status")
async def random_status(response: Response):
    response.status_code = random.choice([200, 200, 300, 400, 500])
    logging.info(f"Random status: {response.status_code}")
    return {"path": "/random_status"}


@app.get("/random_sleep")
async def random_sleep(response: Response):
    sleep_time = random.randint(0, 5)
    time.sleep(sleep_time)
    logging.info(f"Slept for {sleep_time} seconds")
    return {"path": "/random_sleep"}


@app.get("/error_test")
async def error_test(response: Response):
    logging.error("Error encountered in /error_test")
    raise ValueError("A value error occurred")


#if __name__ == "__main__":
#   uvicorn.run(app, host="0.0.0.0", port=int(EXPOSE_PORT))


