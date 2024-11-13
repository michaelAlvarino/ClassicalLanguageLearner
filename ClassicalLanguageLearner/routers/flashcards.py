from fastapi import APIRouter, Depends, HTTPException

from db import flashcards

from ..dependencies import get_token_header

router = APIRouter(
    prefix="/flashcards",
    tags=["flashcards"],
    dependencies=[Depends(get_token_header)],
    responses={404: {"description": "Not found"}},
)


fake_items_db = {"plumbus": {"name": "Plumbus"}, "gun": {"name": "Portal Gun"}}


@router.get("/")
async def read_items():
    return fake_items_db


@router.get("/{flashcard_id}")
async def read_item(flashcard_id: str):
    if flashcard_id not in fake_items_db:
        raise HTTPException(status_code=404, detail="Item not found")
    return {"name": fake_items_db[flashcard_id]["name"], "item_id": flashcard_id}


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