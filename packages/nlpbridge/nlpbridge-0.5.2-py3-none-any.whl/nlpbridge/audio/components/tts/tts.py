r"""text to speech component."""
import uuid
from abc import abstractmethod
from typing import Literal
from urllib.parse import urlencode, quote_plus

import requests

from nlpbridge.audio import logger
from nlpbridge.audio._client import HTTPClient
from nlpbridge.audio._exception import GZUServerException
from nlpbridge.audio.component import AudioBase
from nlpbridge.audio.components.tts.model import TTSInMsg, TTSOutMsg, TTSRequest, TTSResponse
from nlpbridge.audio.message import Message


class BaseTTS(AudioBase):
    def __init__(self, config: dict = None, service_name: str = 'baidu_tts'):
        from nlpbridge.config import CONFIG
        self.config = config if config else CONFIG.dict_config
        self.config = self.config['tts'][service_name]
        self.gateway = self.config['gateway']
        self.api_key = self.config['api_key']
        self.secret_key = self.config['secret_key']
        self.token_url = self.config['token_url']
        self.url = self.gateway
        super().__init__(gateway=self.gateway)

    @abstractmethod
    def run(self, *inputs, **kwargs):
        raise NotImplementedError


class TTS4Gzu(BaseTTS):
    @HTTPClient.check_param
    def run(
            self,
            message: Message,
            timeout: float = None,
            retry: int = 0
    ):
        inp = TTSInMsg(**message.content)
        url = self.url + "?text=" + inp.text
        if retry != self.http_client.retry.total:
            self.http_client.retry.total = retry
        auth_header = self.http_client.auth_header()
        response = self.http_client.session.get(url, timeout=timeout, headers=auth_header, verify=False)
        return response


class TTS4Baidu(BaseTTS):
    def access_token(self):
        try:
            params = {"grant_type": "client_credentials", "client_id": self.api_key, "client_secret": self.secret_key}
            return str(requests.post(self.token_url, params=params).json().get("access_token"))
        except BaseException as e:
            logger.error(f'get access token error: {e}')

    @HTTPClient.check_param
    def run(self,
            message: Message,
            speed: int = 5,
            pitch: int = 5,
            volume: int = 5,
            person: int = 0,
            audio_type: Literal["mp3", "pcm", "wav"] = "wav",
            timeout: float = None,
            retry: int = 0) -> Message:
        inp = TTSInMsg(**message.content)
        request = TTSRequest()
        request.tok = self.access_token()
        request.tex = quote_plus(inp.text)
        request.cuid = str(uuid.uuid4())
        request.ctp = 1
        request.lan = "zh"
        request.spd = speed
        request.pit = pitch
        request.vol = volume
        request.per = person
        # pcm-16k pcm-8k
        format_dict = {3: "mp3", 4: "pcm", 5: "pcm", 6: "wav"}
        aues = [k for k, v in format_dict.items() if v == audio_type]
        request.aue = aues[0] if aues else None
        response = self.__synthesis(request=request, timeout=timeout, retry=retry)
        out = TTSOutMsg(audio_binary=response.binary, audio_type=audio_type)
        return Message(content=out.model_dump())

    def __synthesis(self,
                    request: TTSRequest,
                    timeout: float = None,
                    retry: int = 0
                    ) -> TTSResponse:
        if retry != self.http_client.retry.total:
            self.http_client.retry.total = retry
        auth_header = self.http_client.auth_header()
        auth_header['Content-type'] = "application/json"

        data = TTSRequest.to_dict(request)
        request_data = urlencode(data)
        request_data = request_data.encode('utf-8')
        response = self.http_client.session.post(self.url, params=request_data,
                                                 timeout=timeout, headers=auth_header)
        self.http_client.check_response_header(response)

        request_id = self.http_client.response_request_id(response)
        self.http_client.check_response(response)
        self.__check_service_error(request_id, response)
        return TTSResponse(binary=response.content, request_id=request_id, aue=request.aue)

    @staticmethod
    def __check_service_error(request_id: str, data: dict):
        if "err_no" in data or "err_msg" in data or 'sn' in data or 'idx' in data:
            raise GZUServerException(
                request_id=request_id,
                service_err_code=data.get("err_no", 0),
                service_err_message="{} . {} . {}]".
                format(data.get("err_msg", ""),
                       data.get("sn", ""),
                       data.get("idx", ""))
            )


TTS_SYNTHESISERS = {
    'baidu_tts': TTS4Baidu,
    'gzu_tts': TTS4Gzu
}


class TTS:
    def __init__(self, service_name='baidu_tts', config: dict = None):
        self.config = config
        self.service_name = service_name.lower()
        self.synthesisers = TTS_SYNTHESISERS

    def run(self, message: Message, **kwargs):
        synthesis = self.getSynthesiser()(config=self.config, service_name=self.service_name)
        return synthesis.run(message, **kwargs)

    def getSynthesiser(self):
        if self.service_name not in self.synthesisers:
            raise ValueError(f"Synthesis service '{self.service_name}' is not supported.")
        return self.synthesisers[self.service_name]
