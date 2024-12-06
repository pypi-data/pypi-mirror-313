import sys, os

from nlpbridge.persistent.redis import RedisDB
from tests.text.test_chain import NameTool

sys.path.append(os.getcwd())

from nlpbridge.text.models import GZUBaseLLM
from nlpbridge.text.agent import EasyAgent

# llm = GZUBaseLLM()
# agent = EasyAgent.from_llm(llm=llm, use_memory=False)
# resp = agent.run(inputs={"input": "hello world"})

# print(resp)

# =================================================================================================

import yaml
from langchain.agents.format_scratchpad import format_log_to_str

from langchain_core.messages import HumanMessage, AIMessage
from langchain_core.runnables import RunnablePassthrough
from langchain_core.tools import BaseTool
from langchain_openai import ChatOpenAI

from nlpbridge.persistent.redis import RedisDB
from nlpbridge.text.agent import create_structured_chat_agent
from nlpbridge.text.template_manager import TemplateManager, TemplateGetter
from langchain.agents import AgentExecutor
from nlpbridge.text.models import GZUBaseLLM
from nlpbridge.text.agent import EasyAgent

YAML_PATH= "/Users/apple/vitalis/source_code/midplugin/config.yaml"

# with open('../../config.yaml', 'r') as file:
with open(YAML_PATH, 'r') as file:
    config = yaml.safe_load(file)

OPENAI_BASE_URL = config['chatgpt']['url']
OPENAI_API_KEY = config['chatgpt']['api_key']
os.environ["OPENAI_BASE_URL"] = OPENAI_BASE_URL
os.environ["OPENAI_API_KEY"] = OPENAI_API_KEY

db = RedisDB(config)

template_manager = TemplateManager(db)
template_getter = TemplateGetter(template_manager)

prompt = template_getter.get_chat_prompt_template("template1")

model = ChatOpenAI(model="gpt-3.5-turbo-0125", temperature=0.5)

tools = [NameTool()]

runnables = [prompt, model, NameTool()]

agent = EasyAgent.from_runnables(runnables)
agent.set_chain_structure(runnables)
resp = agent.run(inputs={
        "input": "what's my name?",
        "chat_history": [
            HumanMessage(content="hi! my name is bob"),
            AIMessage(content="Hello Bob! How can I assist you today?")
        ],
    })

print(resp)
