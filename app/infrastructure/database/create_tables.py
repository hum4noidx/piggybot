import logging

from infrastructure.database.base import Base

logger = logging.getLogger(__name__)


async def create_tables(engine):
    async with engine.begin() as conn:
        # await conn.run_sync(Base.metadata.drop_all)
        await conn.run_sync(Base.metadata.create_all)
        logger.info('Tables created')
