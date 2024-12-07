"""
Base Tools
"""
import os
from typing import (
    List,
)

from langchain_community.utilities import SerpAPIWrapper
from langchain_community.vectorstores import Redis
from langchain_core.tools import tool

from nlpbridge.langchain_zhipuai.embeddings.base import ZhipuAIEmbeddings


@tool("web_search")
def web_search(query: str) -> str:
    """A search engine. Useful for when you need to answer questions about current events. Input should be a search query."""
    search = SerpAPIWrapper()
    return search.run(query)


@tool
def rag_google(query: str) -> List[str]:
    """Get google information from the local repository"""
    retriever = Redis(redis_url=os.getenv('REDIS_URL'),
                      index_name=os.getenv("RAG_GOOGLE_INDEX_NAME"),
                      embedding=ZhipuAIEmbeddings()
                      ).as_retriever()
    docs = retriever.invoke(input=query)
    return [doc.page_content for doc in docs]


@tool
def multiply(x: float, y: float) -> float:
    """Multiply 'x' times 'y'."""
    return x * y


@tool
def subtract(x: float, y: float) -> float:
    """subtract 'x' and 'y'."""
    return x - y


@tool
def exponentiate(x: float, y: float) -> float:
    """Raise 'x' to the 'y'."""
    return x ** y


@tool
def add(x: float, y: float) -> float:
    """Add 'x' and 'y'."""
    return x + y


tool_list = {
    'None': 'None',
    'add': add,
    'sub': subtract,
    'exp': exponentiate,
    'mul': multiply
}
