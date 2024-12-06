import sys,os
import yaml
sys.path.append(os.getcwd())
from nlpbridge.persistent.redis import RedisDB

from langchain_community.chat_message_histories import RedisChatMessageHistory
from langchain_core.runnables.history import RunnableWithMessageHistory
from langchain_core.prompts import ChatPromptTemplate, MessagesPlaceholder
from langchain_core.chat_history import BaseMessage
from langchain_openai import ChatOpenAI


# YAML_PATH= "/workspace/xjh/code/GZU4AI/nplbridge/config.yaml"
YAML_PATH = "/Users/apple/vitalis/source_code/midplugin/config.yaml"

with open(YAML_PATH, 'r') as file:
    config = yaml.safe_load(file)

redis = config['redis']
redis["redis_url"] = f"redis://default:{redis['password']}@{redis['url']}:{redis['port']}/{redis['db']}"

system = """你是一个什么都不懂的买房小白，你正要去买自己的房子，但是你对于房子什么都不知道，你就让他(卖房的人)发问一些关于买房的事。

注意：
1.都以不太懂的口吻返回；
2.你的记忆能力不是很好，他前面更你说的一些细节，你记得不是很清楚；
3.以萌新的术语返回；
4.你是一个犹豫，脾气不好的人！！！
"""

system01 = """你是一个初次买房的小白，对买房的流程和细节完全不了解。你感到非常犹豫，并且在面对不确定性时情绪容易激动。你准备购买你的第一套房子，现在需要向房产销售人员询问各种信息。以下是你关心的问题：

房子的基本信息（位置、价格、面积、户型等）。
周边的设施和交通情况。
开发商的背景和信誉。
购房流程和需要准备的文件。
付款方式和贷款选择。
房子的交付时间和装修情况。
是否有优惠或促销活动。
请根据这个设定，与销售人员展开对话，详细询问上述信息。记住，你是一个买房小白，什么都不懂，脾气也不太好，所以尽量问清楚每一个细节，确保自己理解每个步骤和条款。如果回答不满意，务必要表达出你的不满和疑惑。"""

prompt = ChatPromptTemplate.from_messages(
    [
        ("system", system),
        MessagesPlaceholder(variable_name="history_messages"),
        ("human", "{inputs}"),
    ]
)

ChatGPT = ChatOpenAI(api_key=config['chatgpt']['api_key'],base_url=config['chatgpt']['url'])


chain = prompt | ChatGPT


agentId="10003"
def agent(inputs:str):  ## chain_with_history_messages
    chains = RunnableWithMessageHistory(
        chain,
        lambda session_id: RedisChatMessageHistory(
            session_id,
            url=redis["redis_url"],
            key_prefix="history_messages:"
        ),
        input_messages_key="inputs",
        history_messages_key="history_messages",
    )
    config = {"configurable": {"session_id": agentId}}

    res = chains.invoke({"inputs":inputs},config=config)
    print("output:",res)

for _ in iter(int, 1):
    # user_input = input("input: ")
    user_input = "我需要问一下，我想要买一套3000万的住��，请问有什么好的销售��道可以找到吗？"
    agent(user_input)