from fastapi import FastAPI, Depends, APIRouter, Response, Request
from fastapi.responses import FileResponse, StreamingResponse
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from contextlib import asynccontextmanager
import logging


logger = logging.getLogger(__name__)


@asynccontextmanager
async def lifespan(app: FastAPI):
    logger.info("app lifespan")
    await on_init(app)
    logger.info("app on_init done")

    yield

    logger.info("before on_shutdown")
    await on_shutdown(app)
    logger.info("on_shutdown done")


async def on_shutdown(app: FastAPI):
    pass


async def on_init(app: FastAPI):
    pass


router = APIRouter()


@router.get("/download")
async def download(path: str):
    return FileResponse(path)


app = FastAPI(lifespan=lifespan)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(router)
