r"""ASR model.py.
"""
from typing import MutableSequence, List, Any, Optional

import nlpbridge_proto as proto
from pydantic import BaseModel


class ShortSpeechRecognitionRequest(proto.Message):
    r"""    短语音识别标准版的请求体
            format	string	必填	语音文件的格式，pcm/wav/amr/m4a。不区分大小写。推荐pcm文件
            rate	int	    必填	采样率，16000、8000，固定值
            channel	int	    必填	声道数，仅支持单声道，请填写固定值 1
            cuid	string	必填	用户唯一标识，用来区分用户，计算UV值。建议填写能区分用户的机器 MAC 地址或 IMEI 码，长度为60字符以内。
            token	string	必填	开放平台获取到的开发者[access_token]获取 Access Token "access_token")
            dev_pid	int	    选填	不填写lan参数生效，都不填写，默认1537（普通话 输入法模型），见本节识别模型dev_pid参数
            speech	string	必填	本地语音文件的二进制语音数据 ，需要进行base64 编码。与len参数连一起使用。
            len	    int	    必填	本地语音文件的的字节数，单位字节
         """
    format: str = proto.Field(
        proto.STRING,
        number=1,
    )
    rate: int = proto.Field(
        proto.INT64,
        number=2,
    )
    channel: int = proto.Field(
        proto.INT64,
        number=3,
    )
    cuid: str = proto.Field(
        proto.STRING,
        number=4,
    )
    token: str = proto.Field(
        proto.STRING,
        number=5,
    )
    dev_pid: int = proto.Field(
        proto.INT32,
        number=6,
    )
    speech: bytes = proto.Field(
        proto.BYTES,
        number=7,
    )
    len: int = proto.Field(
        proto.INT32,
        number=8,
    )


class ShortSpeechRecognitionResponse(proto.Message):
    r"""短语音识别结果返回体.

         参数:
            request_id(str):
                网关层的请求ID.
            err_no(int):
                算子层的错误码.
            err_msg(str):
                算子层的错误信息.
            corpus_no(str):
            sn(str):
                语音数据唯一标识，系统内部产生。如果反馈及debug请提供sn。
            result(MutableSequence[str]):
                识别结果数组，返回1个最优候选结果。utf-8 编码。
         """
    request_id: str = proto.Field(
        proto.STRING,
        number=1,
    )

    err_no: int = proto.Field(
        proto.INT32,
        number=2,
    )

    err_msg: str = proto.Field(
        proto.STRING,
        number=3,
    )
    corpus_no: str = proto.Field(
        proto.STRING,
        number=4,
    )

    sn: str = proto.Field(
        proto.STRING,
        number=5,
    )
    result: MutableSequence[str] = proto.RepeatedField(
        proto.STRING,
        number=6
    )


class ASRInMsg(BaseModel):
    """ ASR输入message.
        参数:
            raw_audio(bytes):
                原始的语音文件字节数组.

    """
    raw_audio: bytes = None
    audio_url: Optional[str] = None
    audio_path: Optional[str] = None


class ASROutMsg(BaseModel):
    """ ASR输出message.

        参数:
            result(List[str]):
                输出识别后的文本结果.
    """
    result: List[Any]
