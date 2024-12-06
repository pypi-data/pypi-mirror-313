r"""short text to speech model."""
import nlpbridge_proto as proto

from pydantic import BaseModel


class TTSRequest(proto.Message):
    r"""文本转语音请求参数.
            tex	string	必填	合成的文本，文本长度必须小于1024GBK字节。建议每次请求文本不超过120字节，约为60个汉字或者字母数字。
                            请注意计费统计依据：120个GBK字节以内（含120个）记为1次计费调用；每超过120个GBK字节则多记1次计费调用。
                            如需合成更长文本，推荐使用长文本在线合成
            tok  string	必填	开放平台获取到的开发者[access_token]获取 Access Token "access_token")
            cuid string	必填	用户唯一标识，用来计算UV值。建议填写能区分用户的机器 MAC 地址或 IMEI 码，长度为60字符以内
            ctp	 string	必填	客户端类型选择，web端填写固定值1
            lan	 string	必填	固定值zh。语言选择,目前只有中英文混合模式，填写固定值zh
            spd	 int	选填	语速，取值0-15，默认为5中语速
            pit	 int	选填	音调，取值0-15，默认为5中语调
            vol	 int	选填	音量，基础音库取值0-9，精品音库取值0-15，默认为5中音量（取值为0时为音量最小值，并非为无声）
            aue	 int	选填	3为mp3格式(默认)； 4为pcm-16k；5为pcm-8k；6为wav（内容同pcm-16k）;
                            注意aue=4或者6是语音识别要求的格式，但是音频内容不是语音识别要求的自然人发音，所以识别效果会受影响。
            per（基础音库）int	选填	度小宇=1，度小美=0，度逍遥（基础）=3，度丫丫=4
            per（精品音库）int	选填	度逍遥（精品）=5003，度小鹿=5118，度博文=106，度小童=110，度小萌=111，度米朵=103，度小娇=5


    """
    tex: str = proto.Field(
        proto.STRING,
        number=1,
    )
    tok: str = proto.Field(
        proto.STRING,
        number=2,
    )
    cuid: str = proto.Field(
        proto.STRING,
        number=3,
    )
    ctp: int = proto.Field(
        proto.INT32,
        number=4,
    )
    lan: str = proto.Field(
        proto.STRING,
        number=5,
    )
    spd: int = proto.Field(
        proto.INT32,
        number=6,
    )
    pit: int = proto.Field(
        proto.INT32,
        number=7,
    )
    vol: int = proto.Field(
        proto.INT32,
        number=8,
    )
    per: int = proto.Field(
        proto.INT32,
        number=9,
    )
    aue: int = proto.Field(
        proto.INT32,
        number=10,
    )


class TTSResponse(proto.Message):
    r"""文本转语音返回.

         属性:
             binary (bytes): 语音二进制流.
             aue (int):语音格式, 3(mp3), 4(pcm-16k), 5(pcm-8k) 6(wav).
             request_id(str): 请求ID
     """
    binary: bytes = proto.Field(
        proto.BYTES,
        number=1
    )
    aue: int = proto.Field(
        proto.INT32,
        number=2,
    )
    request_id: str = proto.Field(
        proto.STRING,
        number=3,
    )


class TTSInMsg(BaseModel):
    r"""文本转语音输入消息.

        属性:
            text(str): 待转为语音的文本
    """
    text: str


class TTSOutMsg(BaseModel):
    r""" 文本转语音输出消息.

        属性:
            audio_binary(bytes): 语音二进制流.
            audio_type(AudioType): 语音类型，`mp3`或`wav`.
    """
    audio_binary: bytes
    audio_type: str
