from typing import(
    List,
    Optional,
)

from zhipuai import ZhipuAI
from langchain_core.embeddings import Embeddings
from langchain_core.pydantic_v1 import (
    BaseModel,
)

class ZhipuAIEmbeddings(BaseModel, Embeddings):
    """ZhipuAI embedding models.

    To use, you should have the
    environment variable ``ZHIPUAI_API_KEY`` set with your API key or pass it
    as a named parameter to the constructor.

    Example:
        .. code-block:: python

            from langchain_zhipuai import ZhipuAIEmbeddings

            embeddding = ZhipuAIEmbeddings()
    """
    model: str = "embedding-2"

    def embed_documents(
        self, texts: List[str], chunk_size: Optional[int] = 0
    ) -> List[List[float]]:
        """Call out to ZhipuAI's embedding endpoint for embedding search docs.

        Args:
            texts: The list of texts to embed.
            chunk_size: The chunk size of embeddings. If None, will use the chunk size
                specified by the class.

        Returns:
            List of embeddings, one for each text.
        """
        embedding_list = []

        # Iterate over each text in the input list
        for text in texts:
            # Call the ZhipuAI API for each individual text
            zhipuai_embedding = ZhipuAI().embeddings.create(model=self.model, input=text)
            
            # Extract the embedding and append it to the embedding_list
            embedding_list.append(zhipuai_embedding.data[0].embedding)
        
        return embedding_list

    async def aembed_documents(
        self, texts: List[str], chunk_size: Optional[int] = 0
    ) -> List[List[float]]:
        """Call out to OpenAI's embedding endpoint async for embedding search docs.

        Args:
            texts: The list of texts to embed.
            chunk_size: The chunk size of embeddings. If None, will use the chunk size
                specified by the class.

        Returns:
            List of embeddings, one for each text.
        """
        zhipuai_embedding = ZhipuAI().embeddings.create(model=self.model,input=texts)
        """
            change embedding_data type of [embedding[object]] to [[float]]
        """
        embedding_list = [item.embedding for item in zhipuai_embedding.data]
        return embedding_list
        

    def embed_query(self, text: str) -> List[float]:
        """Call out to ZhipuAI's embedding endpoint for embedding query text.

        Args:
            text: The text to embed.

        Returns:
            Embedding for the text.
        """
        return self.embed_documents([text])[0]

    async def aembed_query(self, text: str) -> List[float]:
        """Call out to ZhipuAI's embedding endpoint async for embedding query text.

        Args:
            text: The text to embed.

        Returns:
            Embedding for the text.
        """
        embeddings = await self.aembed_documents([text])
        return embeddings[0]