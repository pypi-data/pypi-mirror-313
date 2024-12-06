import os
from langchain_core.documents import Document
from abc import ABC, abstractmethod
from ws_bom_robot_app.util import timer

class IntegrationStrategy(ABC):
  def __init__(self, knowledgebase_path: str, data: dict[str, str]):
    self.knowledgebase_path = knowledgebase_path
    self.data = data
    self.working_directory = os.path.join(self.knowledgebase_path,self.working_subdirectory())
    os.makedirs(self.working_directory, exist_ok=True)
  @property
  @abstractmethod
  def working_subdirectory(self) -> str:
    pass
  @abstractmethod
  #@timer
  def load(self) -> list[Document]:
    pass
