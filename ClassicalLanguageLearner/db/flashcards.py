from typing import List, Optional
from sqlmodel import Field, SQLModel

class Stack(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)

    name: str
    subject: str

    def __repr__(self) -> str:
        return f"Stack(name={self.name})"

class Flashcard(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)

    stack_id: Optional[int] = Field(default=None, foreign_key="stack.id")

    name: str
    front: bytes
    back: bytes

    def __repr__(self) -> str:
        return f"Flashcard(name={self.name}, front.len={len(self.front)}, back.len={len(self.back)})"
