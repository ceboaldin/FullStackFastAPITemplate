import logging
from contextlib import asynccontextmanager

from asgi_correlation_id import CorrelationIdMiddleware
from fastapi import FastAPI, HTTPException
from fastapi.exception_handlers import http_exception_handler
from appAPI.database import database
from appAPI.logging_conf import configure_logging
from appAPI.routers.post import router as post_router
from appAPI.routers.group import router as group_router

logger = logging.getLogger(__name__)

@asynccontextmanager
async def lifespan(app: FastAPI):
    configure_logging()
    await database.connect()
    yield
    await database.disconnect()

app = FastAPI(lifespan=lifespan)
app.add_middleware(CorrelationIdMiddleware)


app.include_router(post_router)
app.include_router(group_router)


@app.exception_handler(HTTPException)
async def http_exception_handle_logging(request, exc):
    logger.error(f"HTTPException: {exc.status_code} {exc.detail}")
    return await http_exception_handler(request, exc)


