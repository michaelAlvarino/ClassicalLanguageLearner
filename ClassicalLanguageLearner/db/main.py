from sqlalchemy import create_engine
from flashcards import Base

import logging.config

logging.config.fileConfig('logging.conf')
logger = logging.getLogger(__name__)


DATABASE_URL = "postgresql+psycopg://postgres:example@pg:5432"


def main() -> None:
    logger.info("Creating engine")
    e = create_engine(DATABASE_URL)
    logger.info("Creating tables")
    Base.metadata.create_all(e)
    logger.info("Done.")

if __name__ == "__main__":
    main()
