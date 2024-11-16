# setup logging first
import logging
logging.config.fileConfig("logging.conf")

from ClassicalLanguageLearner.db.tools import create_db_and_tables

from contextlib import asynccontextmanager
from fastapi import FastAPI

from ClassicalLanguageLearner.routers import flashcards

@asynccontextmanager
async def lifespan(app: FastAPI):
    create_db_and_tables()
    yield


app = FastAPI(lifespan=lifespan)


app.include_router(flashcards.router)

@app.get("/")
async def root():
    return {"message": "Hola Mundo!"}