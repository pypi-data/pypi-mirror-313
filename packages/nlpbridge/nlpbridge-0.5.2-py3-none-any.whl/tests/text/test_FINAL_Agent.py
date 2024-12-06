'''
## FINAL agent test
'''
import os,sys
sys.path.append(os.getcwd())
from nlpbridge import ChatAgent,RedisDB
from nlpbridge.text.template_manager import TemplateGetter,TemplateManager
from nlpbridge.text.tools import web_search,multiply,exponentiate,add,rag_google
from langchain_openai import ChatOpenAI
from langchain_core.messages import HumanMessage

YAML_PATH = "/Users/apple/vitalis/source_code/nlpbridge/config.yaml"
config = ChatAgent.load_config(YAML_PATH)

llm = ChatOpenAI()
tools = [multiply,add,exponentiate,web_search,rag_google]
prompt = TemplateGetter(TemplateManager(RedisDB(config))).get_chat_prompt_template(field="langchain_prompt",tools=tools)
# prompt = TemplateGetter(TemplateManager(RedisDB(config))).define_chat_prompt_template()

AgentID = "10001"
agent = ChatAgent(
    yaml_path=YAML_PATH,
    agent_id=AgentID,
    llm=llm,
    tools=tools,
    prompt=prompt,
    memory=True
)

def agent_stream(input:str):
    for s in agent.stream(query=input):
        if "__end__" not in s:
            print(s)
            print("-----------")

while True:
    # user_input = input("\nInput: ")
    uesr_input = "ni hao"
    # res = agent.run(query=user_input)
    # print(res,"\n\nInput: ",user_input,"\nOutput:", res['output'])
    
    agent_stream(user_input)
