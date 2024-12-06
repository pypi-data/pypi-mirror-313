# import sys
# import os
# import yaml
# from typing import Dict, Any
# import unittest
# sys.path.append(os.getcwd())
# from nlpbridge import RedisMemory
# from nlpbridge import RedisDB



# def redisConnect()->RedisDB:
#     YAML_PATH= "../../config.yaml"
#     with open(YAML_PATH, 'r') as file:
#         config = yaml.safe_load(file)
#     return RedisDB(config=config,)

# uid = 'unique_user_id'
# agentId = 'agent_identifier'
# redis_memory = RedisMemory(uid, agentId, redisConnect())

# def test_save_context() -> None:
#     """Test save_context method."""
#     inputs = {"input_key1": "input_value1"}
#     outputs = {"output_key1": "output_value1"}
#     redis_memory.save_context(inputs, outputs)
#     counter_key = f"counter:{uid}.{agentId}"
#     redis_key = f"context:{uid}.{agentId}"
    
#     # 验证计数器增加
#     assert redis_memory.redis.client.get(counter_key) == '1'
    
#     # 验证数据保存
#     expected_data = '{"inputs": "input_value1", "outputs": "output_value1"}'
#     print(type(expected_data))
#     print(type(redis_memory.redis.client.hget(redis_key, '1')),redis_memory.redis.client.hget(redis_key, '1'))

# def test_load_memory_variables() -> None:
#     """Test load_memory_variables method."""
#     redis_memory.redis.client.hset(f"context:{uid}.{agentId}", "2", '{"inputs": "input_value2"}, "outputs":  "output_value2"}')
#     result = redis_memory.load_memory_variables(None)
#     expected_data = {
#         "1": '{"inputs":"input_value1"}, "outputs": "output_value1"}',
#         "2": '{"inputs": "input_value2"}, "outputs": "output_value2"}'
#     }
#     print(result)
#     # assert result == expected_data

# def test_memory_variables() -> None:
#     """Test memory_variables method."""
#     redis_memory.redis.client.hset(f"context:{uid}.{agentId}", "2", '{"inputs": "input_value2"}, "outputs": "output_value2"}')
#     result = redis_memory.memory_variables()
#     expected_keys = ['1', '2']
#     assert result == expected_keys

# def test_clear() -> None:
#     """Test clear method."""
#     redis_memory.clear()
#     redis_key = f"context:{uid}.{agentId}"
    
#     # 验证 Redis 键已删除
#     assert redis_memory.redis.client.get(redis_key) is None

# if __name__ == '__main__':
#     test_save_context()
#     test_load_memory_variables()
#     test_memory_variables()
#     test_clear()

import sys,os
import yaml
sys.path.append(os.getcwd())
from nlpbridge.persistent.redis import RedisDB

from langchain_community.chat_message_histories import RedisChatMessageHistory
from langchain_core.runnables.history import RunnableWithMessageHistory
from langchain_core.prompts import ChatPromptTemplate, MessagesPlaceholder
from langchain_core.chat_history import BaseMessage
from langchain_openai import ChatOpenAI


YAML_PATH= "/Users/apple/vitalis/source_code/midplugin/config.yaml"

with open(YAML_PATH, 'r') as file:
    config = yaml.safe_load(file)

redis = config['redis']
# config = config['redis']
redis["redis_url"] = f"redis://default:{redis['password']}@{redis['url']}:{redis['port']}/{redis['db']}"

# history =RedisChatMessageHistory(
#     session_id="chat_1",
#     url = f"redis://default:{config['password']}@{config['url']}:{config['port']}/{config['db']}",
#     key_prefix="history_messages:"
# )

# history.add_ai_message("HI2!!!")
# history.add_user_message("Bye2!!!")
# print(history.messages)

prompt = ChatPromptTemplate.from_messages(
    [
        ("system", "You're an assistant。"),
        MessagesPlaceholder(variable_name="history_messages"),
        ("human", "{inputs}"),
    ]
)

chain = prompt | ChatOpenAI(api_key=config['chatgpt']['api_key'],base_url=config['chatgpt']['url'])

agentId="10002"
chain_with_history = RunnableWithMessageHistory(
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

res = chain_with_history.invoke({"inputs":"Hi! I'm vitalis"},config=config)
print(res)
res = chain_with_history.invoke({"inputs":"Whats my name"},config=config)
print(res)