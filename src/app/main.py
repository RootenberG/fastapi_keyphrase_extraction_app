"""Setup Init app settings and logger"""
import logging
import logging.config
import time
import random
import string
from fastapi import FastAPI
from fastapi.requests import Request
from src.app.views import services
from src.app.services.requests.aiohttp_singleton import SingletonAiohttp
from .db import db

# gets logging settings

# setup loggers
logging.config.fileConfig("logging.conf", disable_existing_loggers=False)

logger = logging.getLogger(__name__)

app = FastAPI(redoc_url=None)  # app init


@app.on_event("startup")
async def on_start_up():
    logger.info("Start aiohttp session and init db")
    SingletonAiohttp.get_aiohttp_client()


@app.on_event("shutdown")
async def on_shutdown():
    logger.info("Close aiohttp session")
    await SingletonAiohttp.close_aiohttp_client()


@app.middleware("http")
async def log_requests(request: Request, call_next):
    """Middleware that store all incoming requests"""
    idem = "".join(
        random.choices(string.ascii_uppercase + string.digits,
                       k=6))  # random id for each user that sends the request
    logger.info(f"rid={idem} start request path={request.url.path}")
    start_time = time.time()

    response = await call_next(request)

    process_time = (time.time() - start_time) * 1000
    formatted_process_time = "{0:.2f}".format(process_time)
    logger.info(
        f"rid={idem} completed_in={formatted_process_time}ms status_code={response.status_code}"
    )

    return response


# endpoints
app.include_router(services.router, prefix="/services", tags=["services"])
db.init_app(app)
