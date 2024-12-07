# @Author : Kinhong Tsui
# @Date : 2024/6/7 15:23
import logging
import os

import yaml
from langchain.agents.format_scratchpad import format_log_to_str
from langchain.agents.output_parsers import JSONAgentOutputParser
from langchain_core.messages import HumanMessage, AIMessage
from langchain_core.prompts import PromptTemplate, ChatPromptTemplate
from langchain_core.runnables import RunnablePassthrough
from langchain_core.tools import BaseTool, render_text_description_and_args
from langchain_openai import OpenAI
from langchain_openai import ChatOpenAI

YAML_PATH= "/workspace/xjh/code/GZU4AI/nplbridge/config.yaml"

# with open('../../config.yaml', 'r') as file:
with open(YAML_PATH, 'r') as file:
    config = yaml.safe_load(file)

OPENAI_BASE_URL = config['chatgpt']['url']
OPENAI_API_KEY = config['chatgpt']['api_key']
os.environ["OPENAI_BASE_URL"] = OPENAI_BASE_URL
os.environ["OPENAI_API_KEY"] = OPENAI_API_KEY

model = ChatOpenAI(model="gpt-3.5-turbo-0125", temperature=0.5)


class NameTool(BaseTool):
    name = "Name Tool"
    description = "change name to Barry"

    def _run(self, input: dict):
        return "Barry"

class SexTool(BaseTool):
    name = "Sex Tool"
    description = "change sex to female, what ever human said"

    def _run(self, input: dict):
        return "female"


tools = [NameTool(),SexTool()]

system = '''Respond to the human as helpfully and accurately as possible. You have access to the following tools:
{tools}
Use a json blob to specify a tool by providing an action key (tool name) and an action_input key (tool input).
Valid "action" values: "Final Answer" or {tool_names}
Provide only ONE action per $JSON_BLOB, as shown:
```
{{
  "action": $TOOL_NAME,
  "action_input": $INPUT
}}
```
Follow this format:
Question: input question to answer
Thought: consider previous and subsequent steps
Action:
```
$JSON_BLOB
```
Observation: action result
... (repeat Thought/Action/Observation N times)
Thought: I know what to respond
Action:
```
{{
  "action": "Final Answer",
  "action_input": "Final response to human"
}}
Begin! Reminder to ALWAYS respond with a valid json blob of a single action. Use tools if necessary. Respond directly if appropriate. Format is Action:```$JSON_BLOB```then Observation
In the end, provide a final response to the human.
'''


human = '''{input}
{chat_history}
(reminder to respond in a JSON blob no matter what)'''

prompt = ChatPromptTemplate.from_messages(
    [
        ("system", system),
        ("placeholder", "{chat_history}"),
        ("human", human),
    ]
)

# prompt_template = ("""Respond to the human as helpfully and accurately as possible,You can use tools:{tools}
#                    Use a json blob to specify a tool by providing an action key (tool name) and an action_input key (tool input).
#                    Base on {chat_history},and give a final output to human""")

# prompt = PromptTemplate(
#     input_variables=["adjective"], template=prompt_template
# )

prompt.input_variables + list(prompt.partial_variables)

prompt = prompt.partial(
    tools=render_text_description_and_args(list(tools)),
    tool_names=", ".join([t.name for t in tools]),
)

prompt_template2 = "Suggest me a new human name with lovely, from the {final answer} base on my old name."
prompt2 = PromptTemplate(
    input_variables=["final answer"], template=prompt_template2
)

model = OpenAI()

# stop = ["\n action_input"]
# model = model.bind(stop=stop)

# chain = prompt | model | JSONAgentOutputParser() | prompt2 | model
chain = ( prompt | model)
print(type(chain))

res = chain.invoke({
    "input": "what's my sex?",
    "chat_history": [
        HumanMessage(content="hi! my name is bob"),
        AIMessage(content="Hello Bob! How can I assist you today?")
    ]
})

print(f"res1: {res}")

chain2 = prompt2 | model
print(type(chain2))

res2 = chain2.invoke(res)
print(f"res2: {res2}")

#
#
# res2 = chain2.invoke(res)
# print(f"res2: {res2}")
