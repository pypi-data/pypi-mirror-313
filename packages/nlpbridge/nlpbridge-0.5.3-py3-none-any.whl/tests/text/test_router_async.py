import asyncio
import os
import random
import sys
import time
from typing import TypedDict

import yaml

sys.path.append(os.getcwd())
from langchain_openai import ChatOpenAI

# YAML_PATH = "/Users/apple/vitalis/source_code/nlpbridge/config.yaml"
# YAML_PATH = "/workspace/xjh/code/GZU4AI/nplbridge/config.yaml"
YAML_PATH = "/Users/wellzhi/Documents/code/nlpbridge/config.yaml"

with open(YAML_PATH, 'r') as file:
    config = yaml.safe_load(file)
redis = config['redis']
config["redis"]["redis_url"] = f"redis://default:{redis['password']}@{redis['url']}:{redis['port']}/{redis['db']}"
os.environ["CONFIG_PATH"] = YAML_PATH
# os.environ["OPENAI_BASE_URL"] = config['chatgpt']['url']
# os.environ["OPENAI_API_KEY"] = config['chatgpt']['api_key']

from nlpbridge import RouterManager, Condition, Node


class NodeCondition(Condition):
    def __call__(self, *args, **kwargs):
        if not random.choice([True, False]):
            return "a1"
        else:
            return "a1"


class SimpleCondition(Condition):
    def __call__(self, node_state: TypedDict) -> str:
        return self.cur_node.name


router_manager = RouterManager()


class ANode(Node):
    async def __call__(self, state: dict) -> TypedDict:
        await asyncio.sleep(1)
        self.user_template_index -= 1
        self._init_agent()
        self.chat_limit -= 1
        # question = input("[Question]: ")
        question = "ni hao"
        response = await self.agent.run(question)
        print(f"[current agent generate]: {response}")
        print(f"[node state]:\n{state}")
        # return {"response":response["output"]}
        return {"context": {"input": question, "response": response.content}}


llm = ChatOpenAI(
    model="ep-20240703064240-n964p",  ## doubao-model by bytedance
    base_url=config['doubao']['url'],
    api_key=config['doubao']['api_key']
)


async def main():
    # random from 1-5
    for router_id in range(1, 6):
        start_time = time.time()
        graph, cfg = await router_manager.get_graph(chat_id="100013", llm=llm, router_id=router_id,
                                              condition_cls=SimpleCondition,
                                              node_cls=ANode)

        # graph, cfg = router_manager.get_graph0(chat_id="100013", llm=llm, router_id=router_id,
        #                                             condition_cls=SimpleCondition,
        #                                             node_cls=ANode)

        # state = graph.get_state(config=cfg)
        # print(f'state:\n{state}')
        # state_next = state.next
        # print()
        # print(f'({state_next[0]}) is current node')
        end_time = time.time()
        print(f"Time elapsed: {end_time - start_time}")


if __name__ == "__main__":
    asyncio.run(main())
