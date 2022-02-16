import logging
from fastapi import FastAPI
from starlette.middleware.cors import CORSMiddleware
from src.todo.router import router as todo_router


app = FastAPI()

LOG = logging.getLogger(__name__)


@app.on_event("startup")
async def startup():
    LOG.debug("App starting...")


@app.on_event("shutdown")
async def shutdown():
    LOG.debug("App shutting down...")


app.add_middleware(
    CORSMiddleware, allow_origins=["*"], allow_methods=["*"], allow_headers=["*"]
)

app.include_router(todo_router)
