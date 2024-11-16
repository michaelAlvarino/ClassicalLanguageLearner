# setup logging first
import logging
logging.config.fileConfig("logging.conf")

from contextlib import asynccontextmanager
from fastapi import Depends, FastAPI
from sqlmodel import Session

from ClassicalLanguageLearner.db.flashcards import Flashcard
from ClassicalLanguageLearner.db.tools import create_db_and_tables, get_engine
from ClassicalLanguageLearner.dependencies import get_query_token, get_token_header
from ClassicalLanguageLearner.internal import admin
from ClassicalLanguageLearner.routers import items, users, flashcards

@asynccontextmanager
async def lifespan(app: FastAPI):
    create_db_and_tables()
    yield


app = FastAPI(dependencies=[Depends(get_query_token)], lifespan=lifespan)


app.include_router(users.router)
app.include_router(items.router)
app.include_router(flashcards.router)
app.include_router(
    admin.router,
    prefix="/admin",
    tags=["admin"],
    dependencies=[Depends(get_token_header)],
    responses={418: {"description": "I'm a teapot"}},
)


@app.get("/")
async def root():
    return {"message": "Hola Mundo!"}