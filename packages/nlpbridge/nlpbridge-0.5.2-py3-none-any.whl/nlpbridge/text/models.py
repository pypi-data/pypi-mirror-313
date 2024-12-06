
# import BaseLanguageModel from langchain
from langchain_core.callbacks import CallbackManagerForLLMRun
from langchain_core.language_models import BaseLanguageModel
from langchain_core.language_models import BaseLLM

from typing import (
    Any,
    List,
    Optional,
)
from langchain_core.outputs import LLMResult
from langchain_core.runnables import Runnable


class GZUBaseLLM(BaseLLM):

    def invoke(self, input, **kwargs):
        resp = self.generate_prompt(input, **kwargs)
        return resp.llm_output['output']

    def generate_prompt(
            self,
            input: str,
            **kwargs: Any,
        ) -> LLMResult:
        llmresult = LLMResult(
            generations=[],
            llm_output={'output':"Your input is:" + input},
            run=[],
        )
        return llmresult

    def _generate(self, prompts: List[str], stop: List[str] = None, run_manager: CallbackManagerForLLMRun = None, **kwargs: Any) -> LLMResult:
        return prompts[0]
    
    def _llm_type(self) -> str:
        return super()._llm_type()