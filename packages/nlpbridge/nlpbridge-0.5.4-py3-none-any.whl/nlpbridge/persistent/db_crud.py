import os
import sys
from typing import Dict, TypeVar, Generic, Union, Any

sys.path.append(os.getcwd())

from nlpbridge.persistent.mysql_dataschema import Template, Router, Node, Edge
from sqlmodel import select, func
from sqlmodel import SQLModel
from nlpbridge.persistent.db import sessionmanager
from sqlalchemy.ext.asyncio import AsyncSession

ModelType = TypeVar("ModelType", bound=SQLModel)


class CRUDBase(Generic[ModelType]):
    def __init__(self, model: type[ModelType]) -> None:
        self.model = model

    async def get_by_id(self, id: int, db_session: AsyncSession = None) -> Union[ModelType, None]:
        async with sessionmanager.session() if db_session is None else db_session as session:
            response = await session.execute(select(self.model).where(self.model.id == id))
            return response.scalar_one_or_none()

    async def get_by_ids(self, list_ids: list[int], db_session: AsyncSession = None) -> Union[list[ModelType], None]:
        async with sessionmanager.session() if db_session is None else db_session as session:
            response = await session.execute(select(self.model).where(self.model.id.in_(list_ids)))
            return response.scalars().all()

    async def get_count(self, db_session: AsyncSession = None) -> Union[int, None]:
        async with sessionmanager.session() if db_session is None else db_session as session:
            response = await session.execute(select(func.count()).select_from(select(self.model).subquery()))
            return response.scalar_one_or_none()

    async def get_multi(self, skip: int = 0, limit: int = 100, db_session: AsyncSession = None) -> list[ModelType]:
        async with sessionmanager.session() if db_session is None else db_session as session:
            query = select(self.model).offset(skip).limit(limit).order_by(self.model.id)
            response = await session.execute(query)
            return response.scalars().all()

    async def create(self, obj_in: Union[ModelType, Dict], db_session: AsyncSession = None) -> ModelType:
        db_obj = self.model.model_validate(obj_in)
        async with sessionmanager.session() if db_session is None else db_session as session:
            session.add(db_obj)
            await session.commit()
            await session.refresh(db_obj)
            return db_obj

    async def update(self, obj_current: ModelType, obj_new: Union[ModelType, Dict[str, Any]],
                     db_session: AsyncSession = None) -> ModelType:
        async with sessionmanager.session() if db_session is None else db_session as session:
            if isinstance(obj_new, dict):
                update_data = obj_new
            else:
                update_data = obj_new.model_dump(exclude_unset=True)
            for field in update_data:
                setattr(obj_current, field, update_data[field])

            session.add(obj_current)
            await session.commit()
            await session.refresh(obj_current)
            return obj_current

    async def delete(self, id: int, db_session: AsyncSession = None) -> ModelType:
        async with sessionmanager.session() if db_session is None else db_session as session:
            response = await session.execute(select(self.model).where(self.model.id == id))
            obj = response.scalar_one()
            await session.delete(obj)
            await session.commit()
            return obj


class CRUDTemplate(CRUDBase):
    def __init__(self) -> None:
        super().__init__(model=Template)


class CRUDRouter(CRUDBase):
    def __init__(self) -> None:
        super().__init__(model=Router)


class CRUDNode(CRUDBase):
    def __init__(self) -> None:
        super().__init__(model=Node)


class CRUDEdge(CRUDBase):
    def __init__(self) -> None:
        super().__init__(model=Edge)
