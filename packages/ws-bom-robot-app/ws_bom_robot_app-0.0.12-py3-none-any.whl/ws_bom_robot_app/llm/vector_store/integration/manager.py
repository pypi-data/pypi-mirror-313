from typing import Type
from ws_bom_robot_app.llm.vector_store.integration.base import IntegrationStrategy
from ws_bom_robot_app.llm.vector_store.integration.sitemap import Sitemap

class IntegrationManager:
  _list: dict[str, Type[IntegrationStrategy]] = {
    "llmkbsitemap": Sitemap,
  }
  @classmethod
  def get_strategy(cls, name: str, knowledgebase_path: str, data: dict[str, str]) -> IntegrationStrategy:
      if name not in cls._list:
          raise ValueError(f"Integration strategy '{name}' not found")
      return cls._list[name](knowledgebase_path, data)
