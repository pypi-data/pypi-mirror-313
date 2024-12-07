import copy
import pydantic

__version__ = '0.0.1'


class SDKReportConfig(pydantic.BaseModel):
    sdk_version: str = __version__
    sdk_language: str = "python"


# report information
default_header = {
    "X-GZU-Sdk-Config": SDKReportConfig().model_dump_json(),
    "X-GZU-Origin": 'gzu_sdk'
}


def get_default_header():
    return copy.deepcopy(default_header)


from nlpbridge.audio._exception import (
    BadRequestException,
    ForbiddenException,
    NotFoundException,
    PreconditionFailedException,
    InternalServerErrorException,
    HTTPConnectionException,
    GZUServerException,
)

from nlpbridge.audio import *
from nlpbridge.audio.message import Message
from nlpbridge.audio.utils.logger_util import logger
from nlpbridge.audio.components.asr.asr import ASR
from nlpbridge.audio.components.tts.tts import TTS

__all__ = [
    # 日志组件
    "logger",
    # 通用入参组件
    "Message",
    # 异常定义
    "BadRequestException",
    "ForbiddenException",
    "NotFoundException",
    "PreconditionFailedException",
    "InternalServerErrorException",
    "HTTPConnectionException",
    "GZUServerException",
    # 语音识别组件
    'ASR',
    'TTS'
]
