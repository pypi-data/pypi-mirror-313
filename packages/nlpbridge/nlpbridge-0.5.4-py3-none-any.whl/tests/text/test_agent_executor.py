# @Author : Kinhong Tsui
# @Date : 2024/6/13 17:23
import os,sys,yaml
sys.path.append(os.getcwd())
from datetime import datetime
from langchain import hub
from langchain.agents import create_structured_chat_agent
from nlpbridge.persistent.redis import RedisDB
from nlpbridge import ChatAgent
from nlpbridge.text.template_manager import TemplateManager, TemplateGetter
from langchain_openai import ChatOpenAI
from langchain_core.runnables.history import RunnableWithMessageHistory
from langchain_community.chat_message_histories import RedisChatMessageHistory
from langchain.agents import AgentExecutor
from nlpbridge.text.tools import web_search,multiply,exponentiate,add,rag_google

os.environ["LANGCHAIN_TRACING_V2"] = "true"
os.environ["LANGCHAIN_PROJECT"] = datetime.now().strftime("%Y-%m-%d")
os.environ["LANGCHAIN_ENDPOINT"] = "https://api.smith.langchain.com"
os.environ["LANGCHAIN_API_KEY"] = "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"
os.environ["OPENAI_BASE_URL"] = "https://api.kwwai.top/v1"
os.environ["OPENAI_API_KEY"]= "sk-uTvkHJWixxfg6lxVEeB32d320e2f413eAbCe2cCaF6D87fF9"
os.environ["REDIS_URL"] = "redis://default:123456@172.22.121.63:30265/0"
os.environ["ZHIPUAI_API_KEY"] = "59e910acc5d4d68b9ef544009d89198d.mUfSMG5h6xgTphfL"
YAML_PATH = "/Users/apple/vitalis/source_code/midplugin/config.yaml"

config = ChatAgent.load_config(YAML_PATH)

db = RedisDB(config)

# prompt = hub.pull("hwchase17/structured-chat-agent")

prompt = TemplateGetter(TemplateManager(db)).get_chat_prompt_template("langchain_prompt")  ##官方指定prompt
tools = [multiply,add,exponentiate,web_search,rag_google]
llm = ChatOpenAI(model="gpt-3.5-turbo-0125", temperature=0.5)

agent = create_structured_chat_agent(llm, tools, prompt)
agent_executor = AgentExecutor(agent=agent, tools=tools, verbose=True,handle_parsing_errors=True,max_iterations=5)

agent_with_chat_history = RunnableWithMessageHistory(
    agent_executor,
    lambda session_id: RedisChatMessageHistory(
        session_id,
        url=os.getenv("REDIS_URL"),
        key_prefix="chat_history:"
    ),
    input_messages_key="input",
    history_messages_key="chat_history",
)

def agant_run(query: str,agentId:str):
    return agent_with_chat_history.invoke(
        {"input":query},
        config={"configurable": {"session_id": agentId}},
    )

AgentID = "10002"
for _ in iter(int, 1):
    # user_input = input("\nInput: ")
    user_input = "How can I find the latest news about AI?"  # example input for testing the agent. You can replace it with your own query.
    res = agant_run(query=user_input,agentId=AgentID)
    print(res,"\n\nInput: ",user_input,"\nOutput:", res['output'])