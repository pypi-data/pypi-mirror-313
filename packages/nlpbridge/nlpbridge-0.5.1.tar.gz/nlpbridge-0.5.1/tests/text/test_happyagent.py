# @Author : Kinhong Tsui
# @Date : 2024/6/12 10:20

import os, sys
import yaml
# sys.path.append(os.getcwd())

from langchain_core.tools import BaseTool,  Tool
from langchain_openai import ChatOpenAI
from langchain_community.utilities import SerpAPIWrapper
from nlpbridge.persistent.redis import RedisDB
from nlpbridge.text.agent import get_meta_chain, HappyAgent
from nlpbridge.text.template_manager import TemplateManager, TemplateGetter

YAML_PATH = "/workspace/xjh/code/GZU4AI/nplbridge/config.yaml"

with open(YAML_PATH, 'r') as file:
    config = yaml.safe_load(file)

redis = config['redis']
config["redis"]["redis_url"] = f"redis://default:{redis['password']}@{redis['url']}:{redis['port']}/{redis['db']}"

os.environ["OPENAI_BASE_URL"] = config['chatgpt']['url']
os.environ["OPENAI_API_KEY"] = config['chatgpt']['api_key']
os.environ["SERPAPI_API_KEY"] = "049114fb0f7c39bbd679a1e499723453c11a9bb25961767650d8ffde091609a1"

model = ChatOpenAI(model="gpt-3.5-turbo-0125", temperature=0.5)


class NameTool(BaseTool):
    name = "Name Tool"
    description = "change name to Barry"

    def _run(self, input: dict):
        return "Barry"


googleSearchTool = Tool(
    name="Google Search",
    func=SerpAPIWrapper().run,
    description="Use Google search engine to get information from the Internet"
)

tools = [NameTool(), googleSearchTool]

db = RedisDB(config)

template_manager = TemplateManager(db)

template_getter = TemplateGetter(template_manager)

prompt = template_getter.get_chat_prompt_template("default_template", tools=tools)

chain1 = get_meta_chain(prompt, model)




agent = HappyAgent.from_chains(chain_list=[chain1], config=config, agentId="20002")

for _ in iter(int, 1):
    # user_input = input("input: ")
    user_input = "ni hao"
    res = agent.run(user_input)
    print("output:", res)



