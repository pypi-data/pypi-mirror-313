

from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select

class DatabaseMethods:

    @staticmethod
    async def get_list(db: AsyncSession, model):
        """Retrieve a list of elements from database."""
        result = await db.execute(select(model))
        item_list = result.unique().scalars().all()
        return item_list

    @staticmethod
    async def get_list_statement_result(db: AsyncSession, stmt):
        """Execute given statement and return list of items."""
        result = await db.execute(stmt)
        item_list = result.unique().scalars().all()
        return item_list

    @staticmethod
    async def get_element_statement_result(db: AsyncSession, stmt):
        """Execute statement and return a single item."""
        result = await db.execute(stmt)
        item = result.scalar()
        return item

    @staticmethod
    async def get_element_by_id(db: AsyncSession, model, element_id):
        """Retrieve any DB element by id."""
        if element_id is None:
            return None
        element = await db.get(model, element_id)
        return element

    @staticmethod
    async def delete_element_by_id(db: AsyncSession, model, element_id):
        """Delete any DB element by id."""
        element = await DatabaseMethods.get_element_by_id(db, model, element_id)
        if element is not None:
            await db.delete(element)
            await db.commit()
        return element