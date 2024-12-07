import os,sys

from langchain_community.chat_message_histories import RedisChatMessageHistory
from langchain_core.runnables.history import RunnableWithMessageHistory
from langchain_core.tools import render_text_description_and_args, BaseTool

from nlpbridge.text.agent import get_meta_chain, HappyAgent, ChatAgent
# sys.path.append(os.getcwd())
from datetime import datetime
from nlpbridge.text.tools import multiply,exponentiate,add,rag_google,subtract,web_search,tool
from langchain_openai import ChatOpenAI

import operator,functools
from typing import Annotated, Sequence, TypedDict,Any,List
from langchain_core.messages import AIMessage, BaseMessage, HumanMessage, ToolMessage
from langchain_core.runnables import RunnableLambda
from langgraph.graph import END, StateGraph 
from langchain_core.prompts import ChatPromptTemplate, MessagesPlaceholder
from langchain.agents import AgentExecutor, create_openai_tools_agent
from langchain.output_parsers.openai_functions import JsonOutputFunctionsParser
from langchain_core.output_parsers import StrOutputParser
from langchain.agents import create_structured_chat_agent
from langchain_core.messages import (
    AIMessage,
    BaseMessage,
    ChatMessage,
    FunctionMessage,
    HumanMessage,
    SystemMessage
)

os.environ["LANGCHAIN_TRACING_V2"] = "true"
os.environ["LANGCHAIN_PROJECT"] = "default"
os.environ["LANGCHAIN_ENDPOINT"] = "https://api.smith.langchain.com"
os.environ["LANGCHAIN_API_KEY"] = "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"
from langsmith import Client
client = Client()

YAML_PATH = "/workspace/xjh/code/GZU4AI/nplbridge/config.yaml"
# YAML_PATH = "/Users/apple/vitalis/source_code/nlpbridge/config.yaml"
config = ChatAgent.load_config(YAML_PATH)



redis = config['redis']
redis["redis_url"] = f"redis://default:{redis['password']}@{redis['url']}:{redis['port']}/{redis['db']}"

llm= ChatOpenAI()

class AgentState(TypedDict):
    messages: Annotated[Sequence[BaseMessage], operator.add]
    next: str


class NameTool(BaseTool):
    name = "Name Tool"
    description = "change name to Barry"

    def _run(self, input: dict):
        return "Barry"

@tool
def add(x: float, y: float) -> float:
    """Add 'x' and 'y'."""
    return x + y

def agent0(state):
    print("Running--agent0")
    while True:
        # qes = input("Current Agent Input: ")
        qes = "ni hao"
        # if "end" in qes:
        #     break
        chat = ChatOpenAI()
        members = ["agent1", "agent2"]
        options = ["end"] + members
        tools = [add]

        prompt = ChatPromptTemplate.from_messages(
            [
                SystemMessage(
                    content='''你是一个风趣幽默的人，说话很机车。根据一下内容回答用户(一下内容不能直接放回给用户)，并且你有{members}，并且你可以使用工具{tools}，去作为节点的选择：

                    你是张伟，一位50岁的成功股票投资者，个人资产达到15亿元人民币，并管理着50亿元人民币的资产。你起初用5000元炒股起家。你现在在与财务顾问交流，讨论设立家族信托以防止子女挥霍财富。

                    现在你接了一个电话，发现你儿子受伤了，心情很暴躁，你现在脾气需要变得暴躁起来。
                    
                    如果你现在心情变好了，就不回答别的，则直接返回"end"这三个字母，没有多余的字段
                    
                     Or should we end? Select one of: {options}
                    '''
                ),
                HumanMessage(
                    content=qes
                ),
                MessagesPlaceholder(variable_name="agent_scratchpad"),
            ]
        ).partial(options=str(options), members=", ".join(members), tools=render_text_description_and_args(list(tools)),  tool_names=", ".join([t.name for t in tools]),)

        agent = create_openai_tools_agent(llm, tools, prompt)
        executor = AgentExecutor(agent=agent, tools=tools)

        chains = RunnableWithMessageHistory(
            executor,
            lambda session_id: RedisChatMessageHistory(
                session_id,
                url=redis["redis_url"],
                key_prefix="history_messages:"
            ),
            input_messages_key="inputs",
            history_messages_key="history_messages",
        )
        config = {"configurable": {"session_id": "33334"}}

        res = chains.invoke({"inputs": qes}, config=config)
        print("output:", res)


        print("\n",res['output'])

        if res['output'] == "end":
            break
    return {"messages": state["messages"],"next": "agent1"}

def agent1(state):
    print("Running--agent1")
    print(state)
    # qes = state["question"]
    while True:
        # qes = input("Current Agent Input: ")
        qes = "ni hao"
        # res = agent.invoke(qes)
        print(qes)
        if "end" in qes:
            break
    return {"messages": state["messages"],"next": "agent2"}

def agent2(state):
    print("Running--agent2")
    # qes = state["question"]
    while True:
        # qes = input("Current Agent Input: ")
        qes = "ni hao"
        # res = agent.invoke(qes)
        print(qes)
        if "end" in qes:
            break
    return {"messages": state["messages"],"next": "agent0"}

workflow = StateGraph(AgentState)
workflow.add_node("agent0", agent0)
workflow.add_node("agent1", agent1)
workflow.add_node("agent2", agent2)
workflow.set_entry_point("agent0")

workflow.add_conditional_edges(
    "agent0",
    lambda x: x['next'],
    {
        "agent0": "agent0",
        "agent1": "agent1",
        "agent2": "agent2",
        "__end__": END,
    }
)
workflow.add_conditional_edges(
    "agent1",
    lambda x: x['next'],
    {
        "agent0": "agent0",
        "agent1": "agent1",
        "agent2": "agent2",
        "__end__": END,
    }
)
workflow.add_conditional_edges(
    "agent2",
    lambda x: x['next'],
    {
        "agent0": "agent0",
        "agent1": "agent1",
        "agent2": "agent2",
        "__end__": END,
    }
)

graph = workflow.compile()

def graph_run(input:str="Graph Start"):
    for s in graph.stream(
        {
            "messages": [
                HumanMessage(content=input)
            ]
        },
        debug= True
    ):
        if "__end__" not in s:
            print(s)
            print("-----------")

for _ in iter(int,1):
    # user_input = input("Input: ")
    # res = graph_run(user_input)
    graph_run()
    print("\n")



# class AgentState(TypedDict):
#     messages: Annotated[Sequence[BaseMessage], operator.add]
#     next: str

# def create_agent(llm: ChatOpenAI, tools: list, system_prompt: str):
#     prompt = ChatPromptTemplate.from_messages(
#         [
#             (
#                 "system",
#                 system_prompt,
#             ),
#             MessagesPlaceholder(variable_name="messages"),
#             MessagesPlaceholder(variable_name="agent_scratchpad"),
#         ]
#     )
#     agent = create_openai_tools_agent(llm, tools, prompt)
#     executor = AgentExecutor(agent=agent, tools=tools)
#     return executor

# def agent_node(state, agent, name):
#     result = agent.invoke(state)
#     print("Current Node Output: ",result["output"])
#     return {"messages": [HumanMessage(content=result["output"], name=name)]}

# members = ["Search_Engine", "Retriever_Google_Information_With_Repositories"]
# system_prompt = (
#     "You are a supervisor tasked with managing a conversation between the"
#     " following workers:  {members}. Given the following user request,"
#     " respond with the worker to act next. Each worker will perform a"
#     " task and respond with their results and status. When finished,"
#     " respond with FINISH."
# )
# options = ["FINISH"] + members
# # Using openai function calling can make output parsing easier for us
# function_def = {
#     "name": "route",
#     "description": "Select the next role.",
#     "parameters": {
#         "title": "routeSchema",
#         "type": "object",
#         "properties": {
#             "next": {
#                 "title": "Next",
#                 "anyOf": [
#                     {"enum": options},
#                 ],
#             }
#         },
#         "required": ["next"],
#     },
# }
# prompt = ChatPromptTemplate.from_messages(
#     [
#         ("system", system_prompt),
#         MessagesPlaceholder(variable_name="messages"),
#         (
#             "system",
#             "Given the conversation above, should we FINISH or who should act next?"
#             "Select one of: {options}",
#         ),
#     ]
# ).partial(options=str(options), members=", ".join(members))

# supervisor_chain = (
#     prompt
#     | llm.bind_functions(functions=[function_def], function_call="route")
#     | JsonOutputFunctionsParser()
# )

# search_engine_agent = create_agent(llm, [web_search], "You are a web search engine.")
# search_engine_node = functools.partial(agent_node, agent=search_engine_agent, name="Search_Engine")

# rag_google_agent = create_agent(llm, [rag_google], "You are a local knowlodge resposity about google info.")
# rag_google_node = functools.partial(agent_node, agent=rag_google_agent, name="Retriever_Google_Information_With_Repositories")


# workflow = StateGraph(AgentState)
# workflow.add_node("Search_Engine", search_engine_node)
# workflow.add_node("Retriever_Google_Information_With_Repositories", rag_google_node)
# workflow.add_node("supervisor", supervisor_chain)

# for member in members:
#     workflow.add_edge(member, "supervisor")

# conditional_map = {k: k for k in members}
# conditional_map["FINISH"] = END
# workflow.add_conditional_edges("supervisor", lambda x: x["next"], conditional_map)

# workflow.set_entry_point("supervisor")

# graph = workflow.compile()

# def graph_run(input:str):
#     for s in graph.stream(
#         {
#             "messages": [
#                 HumanMessage(content=input)
#             ]
#         },
#         debug= True
#     ):
#         if "__end__" not in s:
#             print(s)
#             print("-----------")

# for _ in iter(int,1):
#     user_input = input("Input: ")
#     res = graph_run(user_input)
#     print("\n")











# from nlpbridge.text.agent import HappyAgent
# import nlpbridge.text.agent as agent
# import nlpbridge.text as nlp

# llm = nlp.GZUBaseLLM()
# prompt0 = "dd" # tmplateManager.get_template("chain_root_tmp")
# outparser0 = JsonOutputFunctionsParser()

# chain_root = agent.create_structured_chat_agent(tools=[], llm=llm, output_parser=outparser0)

# cond0_tmp = "tools: [t1, t2], \
#     use above tools to check whether input has the bank related information, if yes, then return me: node1, \
#     elif the input has the money related information then return me: node2, \
#     else return me node0"

# class MetaChain(RunnabSequece):
#     def __init__(self, chain):
#         self.chain = chain
#         self.chat_times = 0
#         self.saver = None

#     def invoke(self):
#         inp = input("Enter")
#         resp = self.chain(inp)
#         print(resp)
#         self.chat_times += 1
#         self.saver.save(inp, resp)
#         output_parser = {'resp': resp, 'input': inp,  'chat_times': self.chat_times}
#         return output_parser


# cond0 = agent.create_structured_chat_agent(tools=[], llm=llm, prompt=cond0_tmp)

# cond0 = {
# out = llm(input)
# if need_save:
#     saver.save(input, output, conv_id)
# }

# defaultchain = node1 = node2 = MetaChain(chain_root)

# workflow = StateGraph(AgentState)

# root cond0 node1 node2 defaultchain

# 0 1 0 0 0 1
# 1 0 1 1 0 0
# 0 1 0 0 0 1
# ....

# # Database:

# # System Templates:
# # tmpIDS1...tmpIDS2...

# # C1... C50
# # C1:
# # Template: chain1:[tmpID1, tmpID2, tmpID3], [tool1, too1, too2, too3]
# # Adjacency matrix:[[]..[]]

# workflow.add_node('root', chain_root)
# workflow.add_node('cond0', cond0)
# workflow.add_node('node1', node1)
# workflow.add_node('node2', node2)
# workflow.add_node("default",defaultchain)
# workflow.set_entry_point("root")
# workflow.nodes
# workflow.add_edge('root', 'cond0')

# def return_next_nodeName():
#     namelist = [node.name for node in edge.get_nodes()]
#     next_node = llm(f'chose one name from {namelist}'+ input)
#     return next_node


# class Edge:
#     def __init__(self) -> None:
#         self.goal = ""
#         self.weight = 0
#         self.start_id = 12
#         self.end_id = 13

    
# class EdgeCondition(Ruannable):
#     def __init__(self):
#         super().__init__()
#         self.edges = []

#     def top3(self, rates:list):
#         # chose top 3 rates:
#         pass

#     def __call__(self, input):
#         sim_rates = [self.embedding_compare(edge.goal, input) for edge in self.edges]
#         top3_edge_ids = top3(sim_rates)
#         weights = [e.weight for e in top3_edge_ids]
#         top_edge = top3_edge_ids[random.randint(0, 3, weights)]
        
#         return top_edge.end_id

# edge_cond = EdgeCondition()







# class Template ():
#     def __init__(self,uid,template_id) -> None:
#         self.uid = uid
#         self.template_id = template_id
#         pass

#     def get_tempalte():
#         pass

#     def save()
















# workflow.add_conditional_edges(
#     "cond0",
#     edge_cond,
#     {
#         "root": "root",
#         "": "next_node",
#         "default": "default"
#     },
# )
# workflow.add_edge('cond0', 'root')

# workflow.add_edge('cond0', 'node1')
# workflow.add_edge('cond0', 'node2')


