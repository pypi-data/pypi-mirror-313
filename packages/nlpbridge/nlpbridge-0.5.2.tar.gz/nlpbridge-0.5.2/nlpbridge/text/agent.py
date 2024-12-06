import logging
from functools import reduce
from typing import Any, Dict, List, Optional
from typing import Union, Sequence

from langchain.agents.format_scratchpad import format_log_to_str
from langchain.agents.output_parsers import JSONAgentOutputParser
from langchain.chains.base import Chain
from langchain_community.chat_message_histories import RedisChatMessageHistory
from langchain_core.embeddings import Embeddings
# use argparse to parse the command line arguments
from langchain_core.language_models import BaseLanguageModel
from langchain_core.memory import BaseMemory
from langchain_core.output_parsers import BaseOutputParser
from langchain_core.prompts import BasePromptTemplate, ChatPromptTemplate
from langchain_core.runnables import *
from langchain_core.runnables.history import RunnableWithMessageHistory
from langchain_core.tools import BaseTool, ToolsRenderer, render_text_description_and_args
# import vectorstore from langchain
from langchain_core.vectorstores import VectorStore

logger = logging.getLogger(__name__)


class EasyAgent(Chain):
    """
    NOTE: Following is the docstring for the Chain class:
    Chain should be used to encode a sequence of calls to components like
    models, document retrievers, other chains, etc., and provide a simple interface
    to this sequence.

    The Chain interface makes it easy to create apps that are:
        - Stateful: add Memory to any Chain to give it state,
        - Observable: pass Callbacks to a Chain to execute additional functionality,
            like logging, outside the main sequence of component calls,
        - Composable: the Chain API is flexible enough that it is easy to combine
            Chains with other components, including other Chains.

    The main methods exposed by chains are:
        - `__call__`: Chains are callable. The `__call__` method is the primary way to
            execute a Chain. This takes inputs as a dictionary and returns a
            dictionary output.
        - `run`: A convenience method that takes inputs as args/kwargs and returns the
            output as a string or object. This method can only be used for a subset of
            chains and cannot return as rich of an output as `__call__`.
    """
    memory: Optional[BaseMemory] = None
    prompt_template_manager: Optional[BasePromptTemplate] = None
    llm: Optional[BaseLanguageModel] = None
    tools: Optional[Dict[str, Any]] = {}
    vectorstore: Optional[VectorStore] = None
    embedding: Optional[Embeddings] = None
    outputParser: Optional[BaseOutputParser] = None
    runnables: Optional[List[Runnable]] = None
    input_key: str = "text"
    output_key: str = "answer"

    @classmethod
    def from_runnables(
            cls,
            runnables: List[Runnable],
            **kwargs: Any,
    ) -> "EasyAgent":
        return cls(runnables=runnables, **kwargs)

    @classmethod
    def from_llm(
            cls,
            llm: BaseLanguageModel,
            **kwargs: Any,
    ) -> "EasyAgent":
        return cls(llm=llm, **kwargs)

    @classmethod
    def from_str(
            cls,
            llm: BaseLanguageModel,
            ss: str,
    ) -> "EasyAgent":
        return cls(llm=llm)

    @property
    def input_keys(self) -> List[str]:
        return [self.input_key]

    @property
    def output_keys(self) -> List[str]:
        return [self.output_key]

    def _call(self, inputs: Dict[str, Any]) -> Dict[str, Any]:
        if self.runnables is not None:
            return self.runnables(inputs)

        default_sequence = RunnableSequence()

        return inputs

    def set_chain_structure(self, runnables: List[Runnable]):
        """
        user can define the chain structure by passing a Runnable object.
        e.g.: RunnableSequence, RunnableParallel, RunnableLambda, etc.

        if runnables is None, the chain will be a simple chain with a single Runnable or default RunnableSequence
        """
        self.runnables = runnables

    def prep_inputs(self, inputs: Union[Dict[str, Any], Any]) -> Dict[str, str]:
        # use memory or not:
        if self.agent_config.use_memory:
            if self.memory is None:
                raise ValueError("Memory is not set. Please set memory before using it.")
            inputs = self.super().prep_inputs(inputs)
            return inputs

        return inputs

    def run(self, inputs: Dict[str, Any], **kwargs) -> str:
        if self.runnables is not None:
            chain = reduce(lambda acc, runnable: acc | runnable, self.runnables)
            return chain.invoke(inputs, **kwargs)
        if self.llm is not None:
            return self.llm.invoke(inputs['input'], **kwargs)

        raise ValueError("No runnables or llm set for the agent")


def create_sequence_structure(runnables: List[Runnable]) -> Runnable:
    """
    create a RunnableSequence structure from the list of runnables
    """
    return RunnableSequence(steps=runnables)


def create_parrallel_structure(runnables: List[Runnable]) -> Runnable:
    """
    create a RunnableParallel structure from the list of runnables
    """
    return RunnableParallel(steps=runnables)


def create_graph_structure(runnables: Dict[str, Runnable]) -> Runnable:
    pass


def create_structured_chat_agent(
        llm: BaseLanguageModel,
        tools: Sequence[BaseTool],
        prompt: ChatPromptTemplate,
        tools_renderer: ToolsRenderer = render_text_description_and_args,
        *,
        stop_sequence: Union[bool, List[str]] = True, ) -> Runnable:
    """
    create a structured chat agent with the given runnables
    """
    missing_vars = {"tools", "tool_names", "agent_scratchpad"}.difference(
        prompt.input_variables + list(prompt.partial_variables)
    )
    if missing_vars:
        raise ValueError(f"Prompt missing required variables: {missing_vars}")

    prompt = prompt.partial(
        tools=tools_renderer(list(tools)),
        tool_names=", ".join([t.name for t in tools]),
    )

    if stop_sequence:
        stop = ["\nObservation"] if stop_sequence is True else stop_sequence
        llm_with_stop = llm.bind(stop=stop)
    else:
        llm_with_stop = llm

    agent = (
            RunnablePassthrough.assign(
                agent_scratchpad=lambda x: format_log_to_str(x["intermediate_steps"]),
            )
            | prompt
            | llm_with_stop
            | JSONAgentOutputParser()
    )

    return agent


class HappyAgent(Chain):
    chain_list: Optional[list[RunnableSequence]] = None
    chains: Optional[RunnableSequence] = None
    chains_with_history: Optional[RunnableWithMessageHistory] = None
    config: Optional[Dict[str, Any]] = None
    memory: bool = True
    history_config: Optional[Dict[str, Any]] = None
    agentId: Optional[str] = None

    input_key: str = "text"
    output_key: str = "answer"

    def __init__(self, /, **kwargs: Any):
        super().__init__(**kwargs)
        if self.chain_list is not None:
            self.set_chains_structure()
        if self.memory:
            self.set_chains_history()
        self.history_config = {"configurable": {"session_id": self.agentId}}

    @classmethod
    def from_chains(
            cls,
            chain_list: list[RunnableSequence],
            **kwargs: Any,
    ) -> "HappyAgent":
        return cls(chain_list=chain_list, **kwargs)  # chain_list, config, agentId, options: memory

    @property
    def input_keys(self) -> List[str]:
        return [self.input_key]

    @property
    def output_keys(self) -> List[str]:
        return [self.output_key]

    def _call(self, inputs: Dict[str, Any]) -> Dict[str, Any]:
        return inputs

    def set_chains_structure(self):
        chains = reduce(lambda acc, runnable_sequence: acc | runnable_sequence, self.chain_list)
        self.chains = chains
        return True

    def set_chains_history(self):
        self.chains_with_history = RunnableWithMessageHistory(
            self.chains,
            lambda session_id: RedisChatMessageHistory(
                session_id,
                url=self.config['redis']["redis_url"],
                key_prefix="history_messages:"
            ),
            input_messages_key="inputs",
            history_messages_key="history_messages",
        )

    def run(self, inputs, memory=True, **kwargs) -> str:
        if memory:
            return self.chains_with_history.invoke({"inputs": inputs}, config=self.history_config)

        return self.chains.invoke(inputs, **kwargs)


def get_meta_chain(prompt: BasePromptTemplate, model: BaseLanguageModel, output_parser: BaseOutputParser = None):
    if output_parser is not None:
        return prompt | model | output_parser

    return prompt | model


####@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@####
from nlpbridge.text.template_manager import init_prompt_with_tools
from nlpbridge.persistent.redis import RedisDB
from datetime import datetime
import os


class ChatAgent:
    def __init__(self, yaml_path: None, agent_id, llm, tools, prompt, memory=False):
        # if yaml_path is None and os.getenv("YAML_PATH") is not None:
        #     yaml_path = os.getenv("YAML_PATH")
        # else:
        #     raise ValueError("YAML_PATH not provided.")
        self.agent_id = agent_id
        self.memory = memory
        self.config = self.load_config(yaml_path)
        self.db = RedisDB(config=self.config)
        self.agent = self.create_agent(llm, tools, prompt)
        self.history = self.setup_message_history()

    @staticmethod
    def load_config(yaml_path: None):
        from nlpbridge.config import CONFIG
        # with open(yaml_path, 'r') as file:
        #     config = yaml.safe_load(file)
        # Update the dynamic parts
        current_date = datetime.now().strftime("%Y-%m-%d")
        CONFIG.os_config.LANGCHAIN_PROJECT = current_date
        for key, value in CONFIG.dict_config['os_config'].items():
            os.environ[key] = value
        return CONFIG

    def create_agent(self, llm, tools, prompt):
        # agent = create_structured_chat_agent(llm, tools, prompt)
        # agent = create_openai_tools_agent(llm,tools, prompt)
        if tools[0] != 'None':
            prompt = init_prompt_with_tools(prompt, tools)
        agent = prompt | llm
        # return AgentExecutor(agent=agent, tools=tools, verbose=True, handle_parsing_errors=True, max_iterations=10)
        return agent

    def setup_message_history(self):
        if self.memory:
            # Setup to handle message history
            return RunnableWithMessageHistory(
                self.agent,
                lambda session_id: RedisChatMessageHistory(
                    session_id,
                    url=f"redis://{self.config.redis.user}:{self.config.redis.password}@{self.config.redis.url}:{self.config.redis.port}/0",
                    ttl=60 * 60 * 24,
                ),
                input_messages_key="input",
                history_messages_key="chat_history"
            )
        else:
            raise ValueError("Message history is disabled, ensure it is enabled before using this method.")

    async def run(self, query):
        # Use the message history system to handle queries
        if self.memory:
            return await self.history.ainvoke({"input": query},
                                       config={"configurable": {"session_id": self.agent_id}})
        else:
            return await self.agent.ainvoke({"input": query})

    def stream(self, query):
        # Use the message history system to handle queries with steam pattern
        if self.memory:
            return self.history.stream({"input": query},
                                       config={"configurable": {"session_id": self.agent_id}})
        else:
            return self.agent.stream({"input": query})

    def interactive_session(self):
        while True:
            # user_input = input("Input: ")
            user_input = "你好呀，你是谁？"
            print("Output:", self.run(user_input))
