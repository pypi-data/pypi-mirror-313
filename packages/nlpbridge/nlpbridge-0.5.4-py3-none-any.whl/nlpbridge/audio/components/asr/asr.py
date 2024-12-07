import json
import json
import traceback
import uuid
from abc import abstractmethod

import logger
import requests

from nlpbridge.audio._client import HTTPClient
from nlpbridge.audio._exception import GZUServerException
from nlpbridge.audio.component import AudioBase
from nlpbridge.audio.components.asr.model import ShortSpeechRecognitionRequest, ShortSpeechRecognitionResponse, \
    ASRInMsg, ASROutMsg
from nlpbridge.audio.message import Message
from nlpbridge.audio.utils.logger_util import logger


class BaseASR(AudioBase):
    def __init__(self, config: dict = None, service_name: str = 'gzu-asr'):
        from nlpbridge.config import CONFIG
        self.config = config if config else CONFIG.dict_config
        self.config = self.config['asr'][service_name]
        self.gateway = self.config['gateway']
        self.api_key = self.config['api_key']
        self.secret_key = self.config['secret_key']
        self.token_url = self.config['token_url']
        self.url = self.gateway
        super().__init__(gateway=self.gateway)

    @abstractmethod
    def run(self, *inputs, **kwargs):
        raise NotImplementedError


class ASR4Baidu(BaseASR):
    def get_access_token(self):
        try:
            params = {"grant_type": "client_credentials", "client_id": self.api_key, "client_secret": self.secret_key}
            return str(requests.post(self.token_url, params=params).json().get("access_token"))
        except BaseException as e:
            logger.error(f'get access token error: {e}')

    @HTTPClient.check_param
    def run(self, message: Message, audio_format: str = "pcm", rate: int = 16000,
            timeout: float = None, retry: int = 0) -> Message:
        inp = ASRInMsg(**message.content)
        request = ShortSpeechRecognitionRequest()
        request.token = self.get_access_token()
        request.format = audio_format
        request.rate = rate
        request.cuid = str(uuid.uuid4())
        request.channel = 1
        request.dev_pid = 80001
        request.speech = inp.raw_audio
        request.len = len(inp.raw_audio) if inp.raw_audio else 0
        response = self._recognize(request, timeout, retry)
        out = ASROutMsg(result=list(response.result))
        return Message(content=out.model_dump())

    def _recognize(self, request: ShortSpeechRecognitionRequest, timeout: float = None,
                   retry: int = 0) -> ShortSpeechRecognitionResponse:
        headers = self.http_client.auth_header()
        headers['content-type'] = 'application/json'
        if retry != self.http_client.retry.total:
            self.http_client.retry.total = retry
        response = self.http_client.session.post(self.url, headers=headers,
                                                 json=ShortSpeechRecognitionRequest.to_dict(request), timeout=timeout)
        self.http_client.check_response_header(response)
        data = response.json()
        self.http_client.check_response(data)
        request_id = self.http_client.response_request_id(response)
        self.__class__._check_service_error(request_id, data)
        response = ShortSpeechRecognitionResponse.from_json(payload=json.dumps(data))
        response.request_id = request_id
        return response

    @staticmethod
    def _check_service_error(request_id: str, data: dict):
        if "err_no" in data and "err_msg" in data:
            if data["err_no"] != 0:
                raise GZUServerException(
                    request_id=request_id,
                    service_err_code=data["err_no"],
                    service_err_message=data["err_msg"]
                )


ASR_RECOGNIZERS = {
    'baidu_asr': ASR4Baidu
}


class ASR:
    def __init__(self, service_name='baidu_asr', config: dict = None):
        self.config = config
        self.service_name = service_name.lower()
        self.recognizers = ASR_RECOGNIZERS

    def run(self, message: Message, **kwargs):
        recognizer = self.getRecognizer()(config=self.config, service_name=self.service_name)
        return recognizer.run(message, **kwargs)

    def getRecognizer(self):
        if self.service_name not in self.recognizers:
            raise ValueError(f"Recognition service '{self.service_name}' is not supported.")
        return self.recognizers[self.service_name]
