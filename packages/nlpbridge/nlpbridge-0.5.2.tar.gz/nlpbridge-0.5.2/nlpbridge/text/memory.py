from langchain_core.memory import BaseMemory
from langchain_core.runnables import Runnable
from nlpbridge.persistent.redis import RedisDB
from typing import (
    Any, Dict, Union,
    List,
    Optional,
)
import json

from nlpbridge.persistent.redis import RedisDB


class Memory(BaseMemory):
    def __init__(self, dbclient):
        self.dbclient = dbclient

    def create(self, key: str, value: Any):
        self.dbclient.set(key, value)

    def get(self, key: str) -> Any:
        return self.dbclient.get(key)
    
    def delete(self, key: str):
        self.dbclient.delete(key)


class RedisMemory(BaseMemory):
    uid: str
    agentId: str
    redis: Optional[RedisDB] | None
    message_key: str
    counter_key: str
    kwargs: Optional[Any] | None
    
    def __init__(self, uid, agentId, redis:Optional[RedisDB] | None, **kwargs: Any):
        super().__init__(uid=uid, agentId=agentId, redis=redis,message_key='',counter_key='',kwargs=kwargs)
        if uid is None or not uid:
            raise ValueError("UID cannot be None or empty")
        if agentId is None or not agentId:
            raise ValueError("Agent ID cannot be None or empty")
        if redis is None:
            raise ValueError("Redis instance cannot be None")

        self.uid = uid
        self.agentId = agentId
        self.redis = redis
        self.message_key = f"context:{self.uid}.{self.agentId}"
        self.counter_key = f"counter:{self.uid}.{self.agentId}"


    def memory_variables(self) -> List[str]:
        return self.redis.hkeys(self.message_key)

    def load_memory_variables(self, inputs: Dict[str, Any]|None) -> Dict[str, Any]:
        # raw_data = self.redis.retrieve_hash(self.message_key)
        # processed_data = {}
        # for key, value in raw_data.items():
        #     processed_data[key] = json.loads(value) if value else None
        # return processed_data
        pass

    def save_context(self, inputs: Dict[str,Any], outputs: Dict[str,str]) -> Any:
        sequence_number = self.redis.client.incr(self.counter_key)
        messages = {f"{sequence_number}": json.dumps({"inputs": list(inputs.values()), "outputs": list(outputs.values())})}
        return self.redis.store(self.message_key,messages)
    
    def clear(self):
        self.redis.delete(self.message_key,None)