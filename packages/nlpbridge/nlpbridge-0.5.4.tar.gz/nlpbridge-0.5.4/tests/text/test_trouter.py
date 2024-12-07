import asyncio
import os
import random
import sys
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


async def create_graph():
    graph, cfg = await router_manager.get_graph(chat_id="100013", llm=llm, router_id=4,
                                                condition_cls=SimpleCondition, node_cls=ANode)
    state = graph.get_state(config=cfg)
    print(f'state:\n{state}')
    state_next = state.next
    print()
    print(f'({state_next[0]}) is current node')
    return graph, cfg


async def run():
    graph, cfg = await create_graph()
    async for output in graph.astream(input=None, config=cfg):
        await asyncio.sleep(1)
        for key, value in output.items():
            print(f"output: {output}")
            print(f"state: {graph.get_state(config=cfg)}")
            print(f"({key})[Response]: {value['context']['response']}\n")

    print("[Dialogue ends]\n")


async def get_graph_img():
    import matplotlib.pyplot as plt
    import matplotlib.image as mpimg
    try:
        graph, cfg = await create_graph()
        image_data = graph.get_graph(xray=True).draw_mermaid_png()

        # Save the image data to a file
        with open('output_image.png', 'wb') as f:
            f.write(image_data)

        # Display the image using matplotlib
        img = mpimg.imread('output_image.png')
        plt.imshow(img)
        plt.axis('off')  # Hide axes
        plt.show()

    except Exception as e:
        # Handle exceptions
        print(f"An error occurred: {e}")


asyncio.run(create_graph())
asyncio.run(run())
asyncio.run(get_graph_img())