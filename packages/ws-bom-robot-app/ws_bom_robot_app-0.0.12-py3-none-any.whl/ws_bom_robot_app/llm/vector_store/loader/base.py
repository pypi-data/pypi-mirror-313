
import asyncio
from ws_bom_robot_app.config import config
from typing import Any, Callable, Generator, Optional, Tuple
from langchain_community.document_loaders import DirectoryLoader
from langchain_community.document_loaders.base import BaseLoader
from langchain_community.document_loaders.merge import MergedDataLoader
from langchain_core.documents import Document
from langchain_unstructured import UnstructuredLoader
from pydantic import BaseModel
from ws_bom_robot_app.llm.vector_store.loader.json_loader import JsonLoader
from ws_bom_robot_app.util import timer
class LoaderConfig(BaseModel):
  loader: type[BaseLoader]
  kwargs: Optional[dict[str, Any]] = {}
  #post_processors: Optional[list[Callable[[str], str]]] = None

class Loader():
  def __init__(self, knowledgebase_path: str):
    self.knowledgebase_path = knowledgebase_path
    self._runtime_options = config.runtime_options()

  _list: dict[str, LoaderConfig | None] = {
    '.json': LoaderConfig(loader=JsonLoader),
    '.csv': LoaderConfig(loader=UnstructuredLoader),
    '.xls': LoaderConfig(loader=UnstructuredLoader),
    '.xlsx': LoaderConfig(loader=UnstructuredLoader),
    '.eml': LoaderConfig(loader=UnstructuredLoader),
    '.msg': LoaderConfig(loader=UnstructuredLoader),
    '.epub': None,
    '.md': LoaderConfig(loader=UnstructuredLoader),
    '.org': None,
    '.odt': None,
    '.ppt': None,
    '.pptx': LoaderConfig(loader=UnstructuredLoader),
    '.txt': LoaderConfig(loader=UnstructuredLoader),
    '.rst': None,
    '.rtf': None,
    '.tsv': None,
    '.text': None,
    '.log': None,
    '.htm': LoaderConfig(loader=UnstructuredLoader),
    '.html': LoaderConfig(loader=UnstructuredLoader),
    '.pdf': LoaderConfig(loader=UnstructuredLoader,kwargs={
       'strategy':'ocr_only', #https://docs.unstructured.io/open-source/core-functionality/partitioning auto,ocr_only,hi_res
       'split_pdf_page': False,
       'chunking_strategy': 'basic',
       'max_characters': 1000000,
       'include_page_breaks': True,
       'include_orig_elements': False}),
    '.png': LoaderConfig(loader=UnstructuredLoader,kwargs={"strategy":"ocr_only"}),
    '.jpg': LoaderConfig(loader=UnstructuredLoader,kwargs={"strategy":"ocr_only"}),
    '.jpeg': LoaderConfig(loader=UnstructuredLoader,kwargs={"strategy":"ocr_only"}),
    '.tiff': None,
    '.doc': None, #see liberoffice dependency
    '.docx': LoaderConfig(loader=UnstructuredLoader),
    '.xml': LoaderConfig(loader=UnstructuredLoader),
    '.js': None,
    '.py': None,
    '.c': None,
    '.cc': None,
    '.cpp': None,
    '.java': None,
    '.cs': None,
    '.php': None,
    '.rb': None,
    '.swift': None,
    '.ts': None,
    '.go': None,
  }

  @staticmethod
  def managed_file_extensions() -> list[str]:
    return [k for k,v in Loader._list.items() if v is not None]

  #@timer
  def __directory_loader(self) -> list[DirectoryLoader]:
    loader_configs = {}
    for ext, loader_config in Loader._list.items():
        if loader_config:
            if all([self._runtime_options.loader_strategy != "",loader_config.kwargs,"strategy" in loader_config.kwargs]): # type: ignore
                loader_config.kwargs["strategy"] = self._runtime_options.loader_strategy # type: ignore
            loader_key = (loader_config.loader, tuple(loader_config.kwargs.items())) # type: ignore
            if loader_key not in loader_configs:
                loader_configs[loader_key] = {
                    "loader_cls": loader_config.loader,
                    "loader_kwargs": loader_config.kwargs,
                    "glob_patterns": []
                }
            loader_configs[loader_key]["glob_patterns"].append(f"**/*{ext}")
    loaders = []

    for loader_config in loader_configs.values():
        loaders.append(
          DirectoryLoader(
            self.knowledgebase_path,
            glob=loader_config["glob_patterns"],
            loader_cls=loader_config["loader_cls"],
            loader_kwargs=loader_config["loader_kwargs"],
            show_progress=self._runtime_options.loader_show_progress,
            recursive=True,
            silent_errors=self._runtime_options.loader_silent_errors,
            use_multithreading=True,
            max_concurrency=4
          )
        )
    return loaders

  #@timer
  async def load(self) -> list[Document]:
    loaders = MergedDataLoader(self.__directory_loader())
    return await loaders.aload()
    #return await asyncio.to_thread(loaders.load)
