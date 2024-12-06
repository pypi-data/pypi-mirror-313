"""Component模块包括组件基类，用户自定义组件需要继承Component类，并至少实现run方法"""

from enum import Enum
from pydantic import BaseModel
from typing import Dict, Any, Optional

from nlpbridge.audio._client import HTTPClient

from nlpbridge.audio.message import Message
from abc import ABC


class Arguments(BaseModel):
    r""""Arguments define Component meta fields"""
    name: str = ""
    tool_desc: Dict[str, Any] = {}

    def extract_values_to_dict(self):
        r"""extract ComponentArguments fields to dict"""
        inputs = {}
        for name, info in self.model_fields.items():
            value = getattr(self, name)
            # 获取 display_name 元数据
            if not info.json_schema_extra:
                continue
            variable_name = info.json_schema_extra.get('variable_name')
            if not variable_name:
                inputs[name] = value
                continue
            # 使用 Enum 成员的实际值
            if isinstance(value, Message):
                inputs[variable_name] = str(value.content)
            elif isinstance(value, Enum):
                inputs[variable_name] = str(value.value)
            else:
                inputs[variable_name] = str(value)
        return inputs


class AudioBase(ABC):
    def __init__(
            self,
            meta: Optional[Arguments] = Arguments(),
            gateway: str = "",
    ):
        self.meta = meta
        self.gateway = gateway
        self._http_client = None

    @property
    def http_client(self):
        if self._http_client is None:
            self._http_client = HTTPClient(self.secret_key, self.gateway)
        return self._http_client
