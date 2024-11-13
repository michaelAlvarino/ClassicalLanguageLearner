from sqlalchemy import String
from sqlalchemy.orm import Mapped, mapped_column
from sqlalchemy.ext.declarative import declarative_base


Base = declarative_base()

class Flashcard(Base):
    __tablename__ = "flashcards"
    id: Mapped[int] = mapped_column(primary_key=True)
    subject: Mapped[str] = mapped_column(String(128))
    name: Mapped[str] = mapped_column(String(128))
    front: Mapped[str] = mapped_column(String(1024))
    back: Mapped[str] = mapped_column(String(1024))

    def __repr__(self) -> str:
        return f"Flashcard(subject={self.subject}, name={self.name}, front={self.front}, back={self.back})"
