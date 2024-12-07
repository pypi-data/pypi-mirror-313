import operator
from typing import Annotated, Sequence, TypedDict
from langchain_core.messages import AIMessage, BaseMessage, HumanMessage, ToolMessage
from langchain_core.runnables import RunnableLambda
from langgraph.graph import END, StateGraph


class AgentState(TypedDict):
    messages: Annotated[Sequence[BaseMessage],operator.add]