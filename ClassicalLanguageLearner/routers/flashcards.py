from fastapi import APIRouter, HTTPException
from sqlmodel import Session
import openai

from ClassicalLanguageLearner.db import flashcards
from ClassicalLanguageLearner.db.tools import get_session
from ClassicalLanguageLearner.llm_interface import get_llm_client

import logging

logger = logging.getLogger()

router = APIRouter(
    prefix="/flashcards",
    tags=["flashcards"],
)


@router.post("/create_stack/")
async def create(name: str, subject: str, count: int):
    assert count < 10, "Cannot create a stack with more than 10 flashcards"
    assert len(subject) < 256, "Cannot create a stack with subject longer than 256 characters"
    stack = flashcards.Stack(name=name, subject=subject)
    client = get_llm_client()
    new_flashcards = client.chat.completions.create(
        model="llama3.2",
        messages=[
            {
                "role": "system",
                "content": "You are a helpful teacher that assists students studying for an exam by creating sets of flashcards."
            },
            {
                "role": "user",
                "content": f"Create a set of {count} flashcards on the following subject: {subject}"
            }
        ]
    )
    logger.info("Flashcards: %s", new_flashcards)


@router.put(
    "/{flashcard_id}",
    tags=["custom"],
    responses={403: {"description": "Operation forbidden"}},
)
async def update_flashcard(name: str, subject: str, front: str, back: str):
    if name != "plumbus":
        raise HTTPException(
            status_code=403, detail="You can only update the item: plumbus"
        )
    fc = flashcards.Flashcard(
        
    )
    return {"item_id": name, "name": "The great Plumbus"}