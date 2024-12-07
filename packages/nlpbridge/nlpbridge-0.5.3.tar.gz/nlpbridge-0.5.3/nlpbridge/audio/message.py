import uuid

from pydantic import BaseModel, Extra
from typing import Optional, TypeVar, Generic


_T = TypeVar("_T")


class Message(BaseModel, Generic[_T], extra=Extra.allow):
    content: Optional[_T] = {}
    name: Optional[str] = "msg"
    mtype: Optional[str] = "dict"
    id: Optional[str] = str(uuid.uuid4())

    def __init__(self, content: Optional[_T] = None, **data):
        if content is not None:
            data['content'] = content
        super().__init__(**data)
        self.mtype = type(self.content).__name__

    def __str__(self):
        return f"Message(name={self.name}, content={self.content}, mtype={self.mtype})"

    def __repr__(self):
        return f"{self.__class__.__name__}(name={self.name!r}, content={self.content!r}, mtype={self.mtype!r})"