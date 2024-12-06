# @Author : Kinhong Tsui
# @Date : 2024/6/3 15:22

from abc import ABC, abstractmethod
from typing import (
    List,
    Sequence,
    Optional,
    Mapping,
    Any
)


class PersistentStore(ABC):
    '''PersistentStore is an abstract class that defines the interface for a persistent storage system.'''

    '''Support hash data type storage'''

    @abstractmethod
    def store(self, key, field_value_pairs: Mapping[any, any], data_type: str) -> bool:
        """Set the given key-value pairs with key in hash."""

    @abstractmethod
    def retrieve(self, key, fields: Sequence[any], data_type: str) -> List[Optional[any]]:
        """Get the values associated with the given fields in hash."""

    @abstractmethod
    def update(self, key, field_value_pairs: Mapping[any, any], data_type: str) -> bool:
        """Set the given key-value pairs with key in hash."""

    @abstractmethod
    def delete(self, key, fields: Sequence[any], data_type: str) -> int:
        """Delete the given fields in hash."""

    '''Support set data type storage'''

    '''Support list data type storage'''

    '''Support zset data type storage'''

# class MySqlDBClient:
#     def __init__(self, config: dict) -> None:
#         try:
#             import sqlalchemy
#         except ImportError:
#             raise ImportError(
#                 "Could not import sqlalchemy python package. "
#                 "Please install it with `pip install SQLAlchemy`."
#             )

#         self.mysql_config = config['mysql']
#         self.user = self.mysql_config['user']
#         self.url = self.mysql_config['url']
#         self.port = self.mysql_config['port']
#         self.password = self.mysql_config['password']
#         self.db = self.mysql_config['db']
#         self.client = sqlalchemy.engine.create_engine(f"mysql+pymysql://{self.user}:{self.password}@{self.url}:{self.port}/{self.db}")
    

#     def get_conn(self):
#         return self.client.connect()