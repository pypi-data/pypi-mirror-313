# @Author : Kinhong Tsui
# @Date : 2024/6/12 16:27
import os,sys
sys.path.append(os.getcwd())
from langchain import hub
from langchain.agents.format_scratchpad import format_log_to_str
from langchain_core.runnables import RunnablePassthrough
from nlpbridge.nlp import Nlp
from nlpbridge.text.agent import get_meta_chain, HappyAgent
from nlpbridge.text.template_manager import init_prompt_with_tools
from nlpbridge.text.tools import name_tool, search_tool,rag_tool_with_google_repository
from langchain import hub

os.environ["LANGCHAIN_TRACING_V2"] = "true"
os.environ["LANGCHAIN_PROJECT"] = "default"
os.environ["LANGCHAIN_ENDPOINT"] = "https://api.smith.langchain.com"
os.environ["LANGCHAIN_API_KEY"] = "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"
from langsmith import Client
client = Client()

# from loguru import logger


YAML_PATH = "/workspace/xjh/code/GZU4AI/nplbridge/config.yaml"
# YAML_PATH = "/Users/apple/vitalis/source_code/midplugin/config.yaml"

nlp = Nlp(yaml_path=YAML_PATH)

tools = [name_tool(),rag_tool_with_google_repository()]

# prompt = hub.pull("hwchase17/structured-chat-agent")
prompt = nlp.template_getter.get_chat_prompt_template("template1", tools=tools)

model = nlp.chat_openai


chain1 = get_meta_chain(prompt, model)

agent = HappyAgent.from_chains(chain_list=[chain1], config=nlp.config, agentId="10001")

for _ in iter(int, 1):
    # user_input = input("input: ")
    user_input = "ni hao"
    res = agent.run(user_input)
    print("output:", res)