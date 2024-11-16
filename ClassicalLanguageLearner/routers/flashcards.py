import asyncio
from typing import List
from fastapi import APIRouter

from ClassicalLanguageLearner.db.flashcards import Flashcard

import logging

from ClassicalLanguageLearner.stack_manager import get_stack_manager

logger = logging.getLogger()

router = APIRouter(
    prefix="/flashcards",
    tags=["flashcards"],
)


MAX_COUNT = 25
MAX_SUBJECT_LEN = 256

STACK_MANAGER = get_stack_manager()

@router.post("/create_stack/")
async def create(language: str, subject: str, count: int) -> List[Flashcard]:
    assert count <= MAX_COUNT, f"Cannot create a stack with more than {MAX_COUNT} flashcards"
    assert len(subject) <= MAX_SUBJECT_LEN, f"Cannot create a stack with subject longer than {MAX_SUBJECT_LEN} characters"

    logger.info("Checking db for results")
    stack_db, cards_db = await STACK_MANAGER.get(subject=subject, language=language, count=count)
    if stack_db:
        logger.info("Results found in db")
        return cards_db
    logger.info("Querying LLM for results")
    _, new_cards = await STACK_MANAGER.create(subject=subject, language=language, count=count)
    return new_cards
