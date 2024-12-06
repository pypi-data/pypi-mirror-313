from langchain_community.vectorstores.faiss import FAISS
from langchain_core.documents import Document
from langchain_core.vectorstores.base import VectorStoreRetriever
from langchain_openai import OpenAIEmbeddings
from typing import Any
import asyncio
from pydantic import SecretStr
from ws_bom_robot_app.util import timer,atimer

class FaissHelper():
    _embedding_model = "text-embedding-3-small"
    _CACHE: dict[str, FAISS] = {}
    @staticmethod
    #@timer
    async def create(documents: list[Document], folder_path: str, api_key: SecretStr) -> None:
      embeddings = OpenAIEmbeddings(api_key=api_key, model=FaissHelper._embedding_model)
      faiss_instance = await asyncio.to_thread(FAISS.from_documents, documents, embeddings)
      await asyncio.to_thread(faiss_instance.save_local, folder_path)
    @staticmethod
    #@timer
    def get_loader(folder_path:str,api_key:SecretStr) -> FAISS:
        """_summary_

        Args:
            folder_path (str): _description_
            api_key (str): _description_

        Returns:
            FAISS: _description_
        """
        if not folder_path in FaissHelper._CACHE:
            _faiss = FAISS.load_local(
                folder_path=folder_path,
                embeddings=OpenAIEmbeddings(api_key=api_key, model=FaissHelper._embedding_model),
                allow_dangerous_deserialization=True
            )
            FaissHelper._CACHE[folder_path] = _faiss
        return FaissHelper._CACHE[folder_path]

    @staticmethod
    #@timer
    def get_retriever(folder_path:str,api_key:SecretStr,search_type=str, search_kwargs= dict[str,Any]) -> VectorStoreRetriever:
        """_summary_

        Args:
            folder_path (str): _description_
            api_key (str): _description_

        Returns:
            VectorStoreRetriever: _description_
        """
        _faiss = FaissHelper.get_loader(folder_path,api_key)
        return _faiss.as_retriever(search_type=search_type, search_kwargs=search_kwargs)
    @staticmethod
    #@atimer
    async def _combine_search(retrievers: list[VectorStoreRetriever], query:str) -> list[Document]:
        """_summary_

        Args:
            list(VectorStoreRetriever): _description_

        Returns:
            list[Document]: _description_
        """
        def _remove_duplicates(docs: list[Document]) -> list[Document]:
            """Remove duplicate documents based on content"""
            seen_contents = set()
            unique_docs = []
            for doc in docs:
                if doc.page_content not in seen_contents:
                    seen_contents.add(doc.page_content)
                    unique_docs.append(doc)
            return unique_docs
        # Perform the searches concurrently
        search_tasks = [retriever.ainvoke(query) for retriever in retrievers]
        search_results = await asyncio.gather(*search_tasks)
        # Combine and de-duplicate the results
        all_docs = _remove_duplicates([doc for docs in search_results for doc in docs])
        return all_docs
    @staticmethod
    #@atimer
    async def invoke(folder_path:str,api_key:SecretStr, query:str, search_type=str, search_kwargs= dict[str,Any]) -> list[Document]:
        """_summary_
        Args:
            folder_path (str): _description_
            api_key (str): _description_
            query (str): _description_
            search_type (str): _description_
            search_kwargs (dict[str,Any]): _description_
              k: Number of documents to retrieve
              fetch_k: Number of documents to fetch for MMR selection (if None, defaults to 2 * k)
              lambda_mult: MMR diversity parameter (0 = max diversity, 1 = max similarity)
        Returns:
            list[Document]: _description_
        """
        if (search_type == "mixed"):
          similarity_retriever = FaissHelper.get_retriever(folder_path,api_key,"similarity",search_kwargs) # type: ignore
          mmr_kwargs = {
            "k": search_kwargs.get("k",4), # type: ignore
            "fetch_k": search_kwargs.get("fetch_k",20), #type: ignore
            "lambda_mult": search_kwargs.get("lambda_mult", 0.2), # type: ignore
          }
          search_kwargs.update(mmr_kwargs)
          mmr_retriever = FaissHelper.get_retriever(folder_path,api_key,"mmr",search_kwargs) # type: ignore
          return await FaissHelper._combine_search([similarity_retriever, mmr_retriever], query)
        return await FaissHelper.get_retriever(folder_path,api_key,search_type,search_kwargs).ainvoke(query)

