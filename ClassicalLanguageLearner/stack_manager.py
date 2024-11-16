from functools import cache
import json
from typing import Callable, Dict, List, Optional, Tuple
from fastapi import logger
from openai import OpenAI
from sqlmodel import Session, select

from ClassicalLanguageLearner.db.flashcards import Flashcard, Stack
from ClassicalLanguageLearner.db.tools import get_engine
from ClassicalLanguageLearner.llm_interface import get_llm_client
from ClassicalLanguageLearner.prompts import FETCH_FLASHCARDS_PROMPT

import logging

logger = logging.getLogger()

MAX_RETRIES = 3
TEMPERATURE = 0

class StackManager:
    def __init__(
            self,
            llm_client: OpenAI,
            model_name: str,
            session_provider: Callable[[], Session]
            ) -> None:
        self.llm_client = llm_client
        self.model_name = model_name
        self.session_provider = session_provider


    async def _generate_cards(self, stack: Stack) -> str:
        """
        Makes a call to an LLM to generate cards, returns the LLM response as a raw string, without attempting to parse
        as an object.
        """
        new_flashcards = self.llm_client.chat.completions.create(
            model=self.model_name,
            temperature=TEMPERATURE,
            messages=[
                {
                    "role": "system",
                    "content": FETCH_FLASHCARDS_PROMPT,
                },
                {
                    "role": "user",
                    "content": f"Subject: {stack.subject}\nLanguage: {stack.language}\nCount: {stack.count}\nFlashcards: ",
                }
            ]
        )
        return new_flashcards.choices[0].message.content


    async def save(self, stack: Stack, flashcards: List[Flashcard]) -> None:
        """
        Save a given stack and flashcards
        """
        for card in flashcards:
            card.stack_id = stack.id
        with Session(get_engine()) as session:
            session.add_all([stack] + flashcards)
            session.commit()


    async def get(self, subject: str, language: str, count: int) -> Tuple[Optional[Stack], Optional[List[Flashcard]]]:
        """
        Return a stack and the associated flashcards if they exist.
        """
        with self.session_provider() as session:
            stmt = select(Stack).where(Stack.subject == subject).where(Stack.count == count).where(Stack.language == language)
            results = session.exec(stmt).one_or_none()
            if not results: return None, None
            if len(results) != 1: raise ValueError("Found more results than expected")
            stack = results[0]
            stmt2 = select(Flashcard).where(Flashcard.stack_id == stack.id)
            return stack, session.exec(stmt2)


    async def create(self, language: str, subject: str, count: int) -> Tuple[Stack, List[Flashcard]]:
        """
        Creates a new stack of flashcards in the given language
        """
        stack = Stack(language=language, subject=subject, count=count)
        for retries in range(1, MAX_RETRIES + 1):
            new_flashcards = await self._generate_cards(stack)
            try:
                flashcard_json = json.loads(new_flashcards)
                flashcards = json_to_flashcards(flashcard_json)
                return stack, flashcards
            except json.JSONDecodeError:
                logger.exception(f"Failed to decode response after {retries} attempts. Failed attempt: {new_flashcards}.")

def json_to_flashcards(json_in: List[Dict[str, str]]) -> List[Flashcard]:
    return [Flashcard(name=item["name"], front=bytes(item["front"], "utf-8"), back=bytes(item["back"], "utf-8")) for item in json_in]


@cache
def get_stack_manager() -> StackManager:
    return StackManager(get_llm_client(), "llama3.2", lambda: Session(get_engine()))

