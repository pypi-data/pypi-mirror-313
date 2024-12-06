import logging
import random
from typing import List, Literal, Optional, TypeVar, TypedDict, Callable, Tuple, Any, Dict, Set
from uuid import uuid4

import numpy as np
from langchain_core.prompts import ChatPromptTemplate, MessagesPlaceholder
from langchain_core.runnables.base import Runnable
from langgraph.checkpoint.memory import MemorySaver
from langgraph.graph import StateGraph, END
from langgraph.graph.graph import CompiledGraph
from sqlalchemy.ext.asyncio import AsyncSession

from nlpbridge import ChatAgent
from nlpbridge.persistent.db_crud import CRUDRouter, CRUDNode, CRUDEdge, CRUDTemplate
from nlpbridge.persistent.mysql_dataschema import Node as NodeModel
from nlpbridge.text.tools import tool_list

memory = MemorySaver()

Input = TypeVar("Input", contravariant=True)
Output = TypeVar("Output", covariant=True)
logger = logging.getLogger(__name__)


class BaseNode:
    id: int
    name: str
    description: str
    goal: str  # node goal
    chat_limit: int
    system_template_ids: List[int]
    user_template_ids: List[int]
    tool_names: List[str]


class Template:
    id: int
    name: str
    type: Literal["user", "sys"] = "user"
    content: str


class Edge:
    id: int
    start_id: int
    end_id: int
    goal: str
    weight: float


def get_sys_template_pair(system_templates) -> Tuple[str, str]:
    start_sys_template = system_templates[0] if len(system_templates) > 0 else None
    end_sys_template = system_templates[1] if len(system_templates) > 1 else None
    return start_sys_template, end_sys_template


class Node(Callable[[dict], TypedDict]):
    def __init__(self, id, name, description, goal, chat_limit, system_template_ids, user_template_ids,
                 system_templates,
                 user_templates, tool_names,
                 in_edges,
                 out_edges,
                 llm,
                 chat_id, **kwargs):
        self.id = id
        self.name = name
        self.description = description
        self.goal = goal
        self.chat_limit = chat_limit
        self.system_templates_ids = system_template_ids
        self.user_templates_ids = user_template_ids
        self.tool_names = tool_names
        self.system_templates = system_templates
        self.user_templates = user_templates
        self.user_template_index = len(user_templates)  # 当前使用user_template的index
        self.in_edges = in_edges
        self.out_edges = out_edges
        self.llm = llm
        self.chat_id = chat_id

    def rand_prompt(self):
        # start_sys_template + user_prompt + end_sys_template
        start_sys_template, end_sys_template = get_sys_template_pair(self.system_templates)

        start_sys_prompt = start_sys_template.content if start_sys_template else ""
        end_sys_prompt = end_sys_template.content if end_sys_template else ""

        user_template = None
        if self.user_templates:
            if self.user_template_index >= 0 and len(self.user_templates) > self.user_template_index:
                user_template = self.user_templates[self.user_template_index]
            else:
                # chat_limit - len(user_templates), 随机选择一个user_template
                user_template = random.choice(self.user_templates)

        user_prompt = user_template.content if user_template else ""
        return ChatPromptTemplate.from_messages(
            [
                ("system", start_sys_prompt + user_prompt + end_sys_prompt),
                MessagesPlaceholder(variable_name="chat_history"),
                ("human", "{input}"),
            ]
        )

    def _set_stop_signal(self, state: dict):
        state["stop"] = True

    def _init_agent(self):
        prompt = self.rand_prompt()
        self.agent = ChatAgent(None, self.chat_id, self.llm, self.tool_names, prompt, True)

    def __call__(self, state: dict) -> Output:
        self.user_template_index -= 1
        self._init_agent()
        self.chat_limit -= 1
        # question = input("[Question]: ")
        question = "你好呀，你是谁？"
        response = self.agent.run(question)
        print(f"[current agent generate]: {response}")
        print(f"[node state]:\n{state}")
        return {"context": {"input": question, "response": response.content}}

    @classmethod
    def init_with_params(cls, id, name, description, goal, chat_limit, system_template_ids, user_template_ids,
                         system_templates,
                         user_templates, tool_names,
                         in_edges,
                         out_edges,
                         llm,
                         chat_id, **kwargs):
        return cls(id, name, description, goal, chat_limit, system_template_ids, user_template_ids,
                   system_templates,
                   user_templates, tool_names,
                   in_edges,
                   out_edges,
                   llm,
                   chat_id, **kwargs)


class DefaultNode(Callable[[dict], TypedDict]):
    def __init__(self):
        self.id = -1
        self.chat_limit = 0
        self.name = "default"

    async def __call__(self, state: dict):
        # default node 暂时只用于退出graph, 后续会补充新功能
        print("------------------- goodbye -------------------")


class Router:
    id: int
    name: str
    node_ids: List[str]
    edge_ids: List[str]
    meta_template_id: str


class NodeManager:

    @staticmethod
    async def get_nodes(node_ids: List[int], db_session: AsyncSession = None) -> List[NodeModel]:
        if not node_ids:
            return []
        return await CRUDNode().get_by_ids(list_ids=node_ids, db_session=db_session)


class EdgeManager:
    @staticmethod
    async def get_edges(edge_ids: List[int], db_session: AsyncSession = None) -> List[Edge]:
        if not edge_ids:
            return []
        return await CRUDEdge().get_by_ids(list_ids=edge_ids, db_session=db_session)


class TemplateManager:
    @staticmethod
    def get_templates(template_ids: List[int], db_session: AsyncSession = None) -> List[Template]:
        if not template_ids:
            return []
        return CRUDTemplate().get_by_ids(list_ids=template_ids, db_session=db_session)


class GraphState(TypedDict):
    nodes: Optional[List[Node]]
    context: Any | Dict[str, Any]


class Condition(Callable[[dict], TypedDict]):
    def __init__(self, cur_node: Node, target_nodes: List[Node]):
        self.cur_node = cur_node
        self.target_nodes = target_nodes

    def call(self, node_state: TypedDict) -> str:
        # Randomly select the next node from the current node and the node pointed to by the node.

        # 如果到graph的末端节点, 此时target node只剩下1个, 就直接返回自己; 并且如果chat_limit<=0就终止
        if len(self.target_nodes[:-1]) < 2:
            if self.cur_node.chat_limit <= 0:
                return self.target_nodes[-1].name
            return self.target_nodes[0].name

        # 更新condition weight
        self.update_condition_weight(node_state)

        # 根据weight进行随机
        weights = self.normalize([edge.weight for edge in self.cur_node.out_edges])

        next = random.choices(self.target_nodes[:-1], weights=weights)[0]
        if next.chat_limit <= 0:
            next = random.choices(self.target_nodes[1:-1], weights=weights[1:])[0]
        logger.debug(f'current node:({self.cur_node.name})[remains]: {self.cur_node.chat_limit}.next:{next.name}')
        return next.name

    def __call__(self, node_state: TypedDict) -> str:
        if node_state.get("stop", False):
            logger.debug(f"stop signal received")
            # return "END"
            return self.target_nodes[-1].name

        return self.call(node_state)

    @classmethod
    def init_with_params(cls, cur_node, target_nodes):
        return cls(cur_node, target_nodes)

    def update_condition_weight(self, node_state) -> None:
        ...

    def normalize(self, weights: list) -> list:
        weights = np.array(weights)

        # 替换所有的零值为一个很小的正值
        epsilon = 1e-10  # 一个很小的值
        weights[weights == 0] = epsilon

        # 归一化，使权重和为1
        normalized_weights = weights / np.sum(weights)

        # 再次确保没有归一化后的权重为零
        if np.any(normalized_weights == 0):
            normalized_weights[normalized_weights == 0] = epsilon
            normalized_weights = normalized_weights / np.sum(normalized_weights)  # 再次归一化

        return normalized_weights


class RouterManager:
    @classmethod
    async def get_router(cls, router_id: int, db_session: AsyncSession = None) -> Router:
        return await CRUDRouter().get_by_id(id=router_id, db_session=db_session)

    @staticmethod
    def get_template_ids(nodes: List[Node]) -> Set[int]:
        template_ids = {
            int(template_id.strip())
            for node in nodes
            for template_list in (node.system_template_ids, node.user_template_ids)
            if template_list
            for template_id in template_list.split(',')
            if template_id.strip()
        }
        return template_ids

    async def get_graph(self, chat_id: str, llm, router_id: int, condition_cls: Condition = Condition,
                        node_cls: Node = Node, recursion_limit: int = 30, db_session: AsyncSession = None, **kwargs) -> \
            Tuple[CompiledGraph, dict]:
        router = await RouterManager.get_router(router_id=router_id, db_session=db_session)
        node_ids = router.node_ids.split(',')
        edge_ids = router.edge_ids.split(',')
        int_node_ids = [int(num) for num in node_ids]
        int_edge_ids = [int(num) for num in edge_ids]

        nodes = await NodeManager.get_nodes(node_ids=int_node_ids, db_session=db_session)
        edges = await EdgeManager.get_edges(edge_ids=int_edge_ids, db_session=db_session)

        template_ids = self.get_template_ids(nodes)
        templates = await TemplateManager.get_templates(template_ids=template_ids, db_session=db_session)

        # Add basic info template
        if router.meta_template_id != None and router.meta_template_id != '':
            meta_template_id = int(router.meta_template_id)
            basic_info_template = await TemplateManager.get_templates([meta_template_id])
            basic_info_template = basic_info_template[0]

            for index, tmp in enumerate(templates):
                if index == 0:
                    tmp.content = f'\n---------------\n{tmp.content}\n\n{basic_info_template.content}\n'
                elif index == len(templates) - 1:
                    continue
                else:
                    tmp.content = f'---------------\n{tmp.content}\n'

        # Convert nodes to runnable nodes
        runnable_nodes = self.convert_to_runnable_node(nodes, edges, templates, llm, chat_id, node_cls, **kwargs)

        # Create default node
        default_node = DefaultNode()
        runnable_nodes.append(default_node)

        # Create and compile the graph
        graph = self._create_graph(runnable_nodes, edges, condition_cls)
        uuid = str(uuid4())
        cfg = {"configurable": {"thread_id": uuid}, "recursion_limit": recursion_limit}
        graph.update_state(config=cfg, values={"nodes": nodes})

        return graph, cfg

    def _create_graph(self, nodes: List[Node], edges: List[Edge], condition_cls: Condition) -> CompiledGraph:
        graph = StateGraph(GraphState)
        for node in nodes:
            node_name = self.get_node_name(node)
            graph.add_node(node_name, node)
        # fixme confirm the start_node and end_node storage
        start_node = nodes[0]
        end_node = nodes[-1]
        graph.set_entry_point(self.get_node_name(start_node))
        graph.set_finish_point(self.get_node_name(end_node))
        self._create_conditional_edges(graph, nodes, edges, condition_cls)

        return graph.compile(checkpointer=memory)

    def _create_conditional_edges(self, graph: StateGraph, nodes: List[Node], edges: List[Edge],
                                  condition_cls: Condition) -> StateGraph:
        exist_start_ids = []
        for edge in edges:
            start_id = edge.start_id
            if start_id in exist_start_ids:
                continue
            exist_start_ids.append(start_id)

            target_edges = [edge for edge in edges if edge.start_id == start_id]
            target_ids = [edge.end_id for edge in target_edges]
            target_nodes = [node for node in nodes if node.id in target_ids]
            target_nodes.append(nodes[-1])
            target_node_names = [self.get_node_name(node) for node in target_nodes]

            cur_node = self.find_node(nodes, edge.start_id)
            cur_node_name = self.get_node_name(cur_node)
            path_map = {name: name for name in target_node_names}

            # add itself
            path_map[cur_node_name] = cur_node_name
            # add node:END to the all nodes:
            # TODO: replace END to Default node.
            path_map["end"] = END
            target_nodes.append(END)

            graph.add_conditional_edges(
                cur_node_name,
                condition_cls.init_with_params(cur_node, target_nodes),
                path_map
            )

        return graph

    @staticmethod
    def get_node_name(node: Node) -> str:
        node_name = node.name
        if node_name == "unnamed":
            if isinstance(node, Runnable):
                node_name = getattr(node, "__name__", node.__class__.__name__)
        return node_name

    @staticmethod
    def find_node(nodes: List[Node], start_id: str) -> Node:
        return next((node for node in nodes if node.id == start_id), None)

    @staticmethod
    def convert_to_runnable_node(nodes: List[NodeModel], edges: List[Edge], templates: List[Template], llm,
                                 chat_id: str, node_cls: Node,
                                 **kwargs) -> List[
        Node]:
        runnable_nodes = []
        for node in nodes:
            system_template_ids = [int(template_id) for template_id in
                                   node.system_template_ids.split(",")] if node.system_template_ids else []
            user_template_ids = [int(template_id) for template_id in
                                 node.user_template_ids.split(",")] if node.user_template_ids else []

            system_templates = [template for template in templates if template.id in system_template_ids]
            user_templates = [template for template in templates if template.id in user_template_ids]

            in_edges = [edge for edge in edges if edge.end_id == node.id]
            out_edges = [edge for edge in edges if edge.start_id == node.id]
            tools = [tool_list[name] for name in node.tool_names.split(",")] if node.tool_names else []

            runnable_node = node_cls.init_with_params(
                node.id,
                node.name,
                node.description,
                node.goal,
                node.chat_limit,
                system_template_ids,
                user_template_ids,
                system_templates,
                user_templates,
                tools,
                in_edges,
                out_edges,
                llm,
                chat_id,
                **kwargs
            )
            runnable_nodes.append(runnable_node)
        return runnable_nodes
