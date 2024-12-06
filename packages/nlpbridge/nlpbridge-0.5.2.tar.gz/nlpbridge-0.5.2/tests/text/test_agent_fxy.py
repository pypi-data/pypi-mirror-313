import sys,os
sys.path.append(os.getcwd())

import yaml
YAML_PATH = r"D:\pythonproject\nlpbridge\config.yaml"
with open(YAML_PATH, 'r') as file:
    config = yaml.safe_load(file)

api_key = "sk-3652b7a412854d5bbd73941475e6a4f8"
base_url = "https://dashscope.aliyuncs.com/compatible-mode/v1"
model = "qwen-turbo"

from langchain_community.chat_message_histories import RedisChatMessageHistory
from langchain_core.runnables.history import RunnableWithMessageHistory
from langchain_core.prompts import ChatPromptTemplate, MessagesPlaceholder
from langchain_core.chat_history import BaseMessage
from langchain_openai import ChatOpenAI


redis = config['redis']
redis["redis_url"] = f"redis://default:{redis['password']}@{redis['url']}:{redis['port']}/{redis['db']}"

system_template1 = """[任务]：现在我们在进行一个角色扮演游戏，注意，这里十分真实，你一定要记住你就是这个角色，不要回答和你角色设定无关的信息。 

[你的设定]："""

user_template = """你是[张伟]，一位50岁的成功股票投资者，个人资产达到15亿人民币，并管理着50亿人民币的资产。你起初用5000元炒股起家。你现在在与家族信托的[销售]交流，讨论设立家族信托以防止子女挥霍财富。你不懂家族信托，你的知识面有限，你的知识只涉及与股票相关的，你的回答除了股票知识外，只有家常的聊天知识。
"""

system_template2 = """
我会扮演[销售]人员，我的问题以下面的方式告诉你，你需要进行回答，注意，如果[销售]的问题和你的目的无关，就拒绝回答，并且不要回答超出你知识范围的内容，要把话题拉回到你的目的上。
[回答字数限制]：你的回答不要超过3句话。
[销售]：[张伟]，"""

prompt = ChatPromptTemplate.from_messages(
    [
        ("system", system_template1+user_template+system_template2),
        MessagesPlaceholder(variable_name="history_messages"),
        ("human", "{inputs}"),
    ]
)

ChatGPT = ChatOpenAI(api_key=api_key, base_url=base_url, model=model)


chain = prompt | ChatGPT
agentId="10011"
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
    print("output:",res.content)

for _ in iter(int, 1):
    user_input = input("input: ")
    # user_input = "我需要问一下，我想要买一套3000万的住��，请问有什么好的销售��道可以找到吗？"
    agent(user_input)