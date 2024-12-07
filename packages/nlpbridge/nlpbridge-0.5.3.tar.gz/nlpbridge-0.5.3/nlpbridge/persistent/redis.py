# # @Author : Kinhong Tsui
# # @Date : 2024/6/3 15:41
from typing import Sequence, Tuple

import yaml
from typing import(
    Any,
    List,
    Sequence,
    cast,
    Optional,
    Tuple,
    Mapping,
)
from typing_extensions import(
    TypeAlias,
)
from langchain_community.storage import RedisStore
from langchain_community.utilities.redis import get_client
from nlpbridge.persistent.persistent_store import PersistentStore
import logger

# _Value: TypeAlias = bytes | float | int | str
# _Key: TypeAlias = str | bytes

class RedisDB(PersistentStore,RedisStore):
    def __init__(self,config):
        self.redis_config = config.dict_config['redis']
        self.url = self.redis_config['url']
        self.port = self.redis_config['port']
        self.password = self.redis_config['password']
        self.db = self.redis_config['db']
        self.redis_url = f"redis://default:{self.password}@{self.url}:{self.port}/{self.db}"

        try:
            import redis
        except ImportError:
            raise ImportError(
                "Could not import redis python package. "
                "Please install it with `pip install redis`."
            )

        try:
            self.client = get_client(redis_url=self.redis_url,decode_responses=True)
        except redis.exceptions.ConnectionError as error:
            logger.error(error)



    '''Support hash data type storage'''
    def store(self, key, field_value_pairs: Mapping[str, str], data_type:str="hash") -> bool:
        """Set the given key-value pairs with key in hash."""
        if data_type == "hash":
            return self.client.hmset(key, field_value_pairs)
        else:
            return None

    def retrieve(self, key, fields: Sequence[str], data_type:str="hash") -> List[Optional[str]]:
        """Get the values associated with the given fields in hash."""
        if data_type == "hash":
            return cast(List[Optional[str]], self.client.hmget(key, fields))
        else:
            return None

    def update(self, key, field_value_pairs: Mapping[str, str], data_type:str="hash") -> bool:
        """Set the given key-value pairs with key in hash."""
        if data_type == "hash":
            return self.client.hmset(key, field_value_pairs)
        else:
            return None

    def delete(self, key, fields: Optional[Sequence[str]], data_type:str="hash") -> int:
        """Delete the given keys."""
        if data_type == "hash":
            if fields is None:
                return self.client.delete(key)
            return self.client.hdel(key, *fields)
        else:
            return None

    def hkeys(self, key) -> List[str]:
        """Get the values associated with the given fields in hash."""
        return self.client.hkeys(key)

    '''Support set data type storage'''

    '''Support list data type storage'''

    '''Support zset data type storage'''
