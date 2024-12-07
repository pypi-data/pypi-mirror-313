# @Author : Kinhong Tsui
# @Date : 2024/6/12 16:01

import yaml
import os, sys

from nlpbridge.persistent.redis import RedisDB
from nlpbridge.text.template_manager import TemplateManager, TemplateGetter
from langchain_openai import ChatOpenAI
from langchain_community.llms import ChatGLM

sys.path.append(os.getcwd())


class Nlp:
    def __init__(self, yaml_path):
        with open(yaml_path, 'r') as file:
            self.config = yaml.safe_load(file)
        self.redis = self.config['redis']
        self.config["redis"][
            "redis_url"] = f"redis://default:{self.redis['password']}@{self.redis['url']}:{self.redis['port']}/{self.redis['db']}"

        os.environ["OPENAI_BASE_URL"] = self.config['chatgpt']['url']
        os.environ["OPENAI_API_KEY"] = self.config['chatgpt']['api_key']


        self.db = RedisDB(self.config)
        self.template_manager = TemplateManager(self.db)
        self.template_getter = TemplateGetter(self.template_manager)
        self.chat_openai = ChatOpenAI(model="gpt-3.5-turbo-0125", temperature=0.5)
        self.chatglm = ChatGLM(
            endpoint_url=f"{self.config['chatglm']['url']}:{self.config['chatglm']['port']}",
            max_token=80000,
            top_p=0.9
        )

