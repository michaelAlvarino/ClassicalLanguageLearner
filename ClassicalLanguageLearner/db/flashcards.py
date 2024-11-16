from typing import Optional
from sqlmodel import Field, SQLModel

class Stack(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)

    language: str
    subject: str
    count: int

    def __repr__(self) -> str:
        return f"Stack(language={self.language}, subject={self.subject}, count={self.count})"

class Flashcard(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)

    stack_id: Optional[int] = Field(default=None, foreign_key="stack.id")

    front: bytes
    back: bytes

    def __repr__(self) -> str:
        return f"Flashcard(front.len={len(self.front)}, back.len={len(self.back)})"
