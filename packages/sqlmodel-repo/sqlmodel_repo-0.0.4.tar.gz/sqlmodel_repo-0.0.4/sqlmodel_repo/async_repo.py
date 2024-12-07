from typing import Optional, Type

from fastapi.exceptions import HTTPException
from sqlalchemy.ext.asyncio import AsyncEngine
from sqlmodel import SQLModel, select, delete, update, func
from sqlmodel.ext.asyncio.session import AsyncSession


# Helper function for AsyncSession
async def get_async_session(db_engine: AsyncEngine) -> AsyncSession:
    """
    Get an asynchronous SQLAlchemy session.

    Args:
        db_engine (AsyncEngine): The async database engine.
    """
    async with AsyncSession(db_engine) as session:
        yield session


class AsyncSQLModelRepo:
    def __init__(
        self,
        model: Type[SQLModel],
        db_engine: AsyncEngine,
        init_stmt=None,
        session: Optional[AsyncSession] = None
    ):
        """
        Generic repository for SQLModel with async database access.

        Args:
            model (Type[SQLModel]): The SQLModel table class.
            db_engine (AsyncEngine): The async SQLAlchemy engine linked to the database.
        """
        self.model = model
        self._init_stmt = init_stmt
        self.db_engine = db_engine
        self.session = session

    def __call__(self, session: AsyncSession):
        """Return a new repository instance tied to a specific session."""
        new_repo = AsyncSQLModelRepo(model=self.model, db_engine=self.db_engine)
        new_repo.session = session
        return new_repo

    async def create(self, **kwargs):
        """Create a new record and save it to the database asynchronously."""
        instance = self.model(**kwargs)
        async with AsyncSession(self.db_engine) as session:
            async with session.begin():  # Begin a transaction
                session.add(instance)
            await session.refresh(instance)
        return instance

    async def get_by_id(self, id: int, *fields):
        """Fetch an object by its primary key asynchronously."""
        stmt = self.init_stmt(*fields).where(getattr(self.model, 'id') == id)
        async with AsyncSession(self.db_engine) as session:
            result = await session.exec(stmt)
        return result.first()

    async def save(self, instance):
        """Save the current object (instance) to the database asynchronously."""
        async with AsyncSession(self.db_engine) as session:
            async with session.begin():
                session.add(instance)
            await session.refresh(instance)

    async def save_or_update(self, instance):
        """Save or update the current object (instance) asynchronously."""
        async with AsyncSession(self.db_engine) as session:
            async with session.begin():
                stmt = select(self.model).where(self.model.id == instance.id)
                result = await session.exec(stmt)
                existing_obj = result.first()

                if existing_obj:
                    for k, v in instance.model_dump().items():
                        setattr(existing_obj, k, v)
                    instance = existing_obj  # Modify the existing object
                session.add(instance)
            await session.refresh(instance)

    async def update(self, id: int, **kwargs):
        """Perform partial update on a record asynchronously."""
        async with AsyncSession(self.db_engine) as session:
            async with session.begin():
                stmt = update(self.model).where(self.model.id == id).values(**kwargs)
                await session.exec(stmt)

    async def update_all(self, **kwargs):
        """Perform a partial update for all selected records asynchronously."""
        async with AsyncSession(self.db_engine) as session:
            async with session.begin():
                if self._init_stmt is not None:
                    stmt = update(self.model).where(self.init_stmt().whereclause).values(**kwargs)
                else:
                    stmt = update(self.model).values(**kwargs)
                await session.exec(stmt)

    async def delete(self, instance):
        """Delete an object from the database asynchronously."""
        async with AsyncSession(self.db_engine) as session:
            async with session.begin():
                await session.delete(instance)

    async def delete_all(self):
        """Delete all records in the query asynchronously."""
        async with AsyncSession(self.db_engine) as session:
            async with session.begin():
                if self._init_stmt is not None:
                    stmt = delete(self.model).where(self.init_stmt().whereclause)
                else:
                    stmt = delete(self.model)
                await session.exec(stmt)

    def filter(self, *filters, _fields=(), **kwargs) -> 'AsyncSQLModelRepo':
        """Filter records based on provided conditions."""
        stmt = self.init_stmt(*_fields).where(
            *filters,
            *[getattr(self.model, k) == v for k, v in kwargs.items()]
        )
        return AsyncSQLModelRepo(
            init_stmt=stmt,
            model=self.model,
            db_engine=self.db_engine,
            session=self.session,
        )

    async def paginate(
        self,
        offset: int = 0,
        limit: int = 50,
        order_by: Optional[str] = None,
        desc: bool = False,
    ) -> list:
        """Paginate results asynchronously."""
        async with AsyncSession(self.db_engine) as session:
            return await self._paginate(session, offset, limit, order_by, desc)

    async def paginate_with_total(
        self,
        offset: int = 0,
        limit: int = 50,
        order_by: Optional[str] = None,
        desc: bool = False,
    ) -> (list, int):
        """Paginate results and fetch total count asynchronously."""
        async with AsyncSession(self.db_engine) as session:
            count_stmt = select(func.count()).select_from(self.init_stmt().subquery())
            result = await session.exec(count_stmt)
            count = result.first()
            items = await self._paginate(session, offset, limit, order_by, desc)
            return items, count

    async def _paginate(
        self,
        session: AsyncSession,
        offset: int = 0,
        limit: Optional[int] = None,
        order_by: Optional[str] = None,
        desc: bool = False,
    ) -> list:
        stmt = self.init_stmt()
        if order_by:
            order = getattr(self.model, order_by).desc() if desc else getattr(self.model, order_by)
            stmt = stmt.order_by(order)
        stmt = stmt.offset(offset).limit(limit) if limit else stmt
        result = await session.exec(stmt)
        return result.all()

    async def all(self) -> list:
        """Fetch all the results asynchronously."""
        async with AsyncSession(self.db_engine) as session:
            result = await session.exec(self.init_stmt())
        return result.all()

    async def count(self):
        """Get the total count of results asynchronously."""
        async with AsyncSession(self.db_engine) as session:
            count_stmt = select(func.count()).select_from(self.init_stmt().subquery())
            result = await session.exec(count_stmt)
        return result.one()

    async def first(self):
        """Fetch the first result asynchronously."""
        async with AsyncSession(self.db_engine) as session:
            result = await session.exec(self.init_stmt())
        return result.first()

    async def get_or_404(self, id: int):
        """Get an object by id or raise a 404 error if not found asynchronously."""
        obj = await self.get_by_id(id)
        if not obj:
            raise HTTPException(
                status_code=404,
                detail=f"{self.model.__name__} with id {id} not found"
            )
        return obj

    async def delete_or_404(self, id: int):
        """Delete an object by id or raise a 404 error if not found asynchronously."""
        obj = await self.get_or_404(id)
        await self.delete(obj)

    async def update_or_404(self, id: int, **kwargs):
        """Update an object by id or raise a 404 error if not found asynchronously."""
        await self.get_or_404(id)
        await self.update(id, **kwargs)

    def _get_select_obj(self, fields=None):
        return (
            [self.model] if not fields
            else [getattr(self.model, f) for f in fields]
        )

    def init_stmt(self, *fields):
        """Initialize a SQL query statement."""
        if self._init_stmt is not None:
            return self._init_stmt
        else:
            return select(*self._get_select_obj(fields))
