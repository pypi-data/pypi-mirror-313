from typing import  Optional, Type
from ws_bom_robot_app.llm.models.api import LlmAppTool
from ws_bom_robot_app.llm.utils.faiss_helper import FaissHelper
from ws_bom_robot_app.llm.tools.utils import getRandomWaitingMessage, translate_text
from ws_bom_robot_app.llm.tools.models.main import ImageGeneratorInput
from pydantic import BaseModel, ConfigDict
from langchain_community.utilities.dalle_image_generator import DallEAPIWrapper

class ToolConfig(BaseModel):
    function: callable
    model: Optional[Type[BaseModel]] = None
    model_config = ConfigDict(
        arbitrary_types_allowed=True
    )

class ToolManager:

    def __init__(
        self,
        app_tool: LlmAppTool,
        api_key: str,
        callbacks: list,
    ):
        self.app_tool = app_tool
        self.api_key = api_key
        self.callbacks = callbacks


    #region functions
    async def document_retriever(self, query: str):
        if (
            self.app_tool.type == "function" and self.app_tool.vector_db
            #and self.settings.get("dataSource") == "knowledgebase"
        ):
            search_type = "similarity"
            search_kwargs = {"k": 4}
            if self.app_tool.search_settings:
                search_settings = self.app_tool.search_settings # type: ignore
                if search_settings.search_type == "similarityScoreThreshold":
                    search_type = "similarity_score_threshold"
                    search_kwargs = {
                        "score_threshold": search_settings.score_threshold_id if search_settings.score_threshold_id else  0.5,
                        "k": search_settings.search_k if search_settings.search_k else 100
                    }
                elif search_settings.search_type == "mmr":
                    search_type = "mmr"
                    search_kwargs = {"k": search_settings.search_k if search_settings.search_k else 4}
                elif search_settings.search_type == "default":
                    search_type = "similarity"
                    search_kwargs = {"k": search_settings.search_k if search_settings.search_k else 4}
                else:
                    search_type = "mixed"
                    search_kwargs = {"k": search_settings.search_k if search_settings.search_k else 4}
            getRandomWaitingMessage(self.app_tool.waiting_message, traduction=False)
            return await FaissHelper.invoke(self.app_tool.vector_db, self.api_key, query, search_type, search_kwargs)
        return []
        #raise ValueError(f"Invalid configuration for {self.settings.name} tool of type {self.settings.type}. Must be a function or vector db not found.")

    async def image_generator(self, query: str, language: str = "it"):
        model = self.app_tool.model or "dall-e-3"
        random_waiting_message = getRandomWaitingMessage(self.app_tool.waiting_message, traduction=False)
        if not language:
            language = "it"
        await translate_text(
            self.api_key, language, random_waiting_message, self.callbacks
        )
        try:
            image_url = DallEAPIWrapper(api_key=self.api_key, model=model).run(query)  # type: ignore
            return image_url
        except Exception as e:
            return f"Error: {str(e)}"

    #endregion

    #class variables (static)
    _list: dict[str,ToolConfig] = {
        "document_retriever": ToolConfig(function=document_retriever),
        "image_generator": ToolConfig(function=image_generator, model=ImageGeneratorInput),
    }

    #instance methods
    def get_coroutine(self):
        tool_cfg = self._list.get(self.app_tool.function_name)
        return getattr(self, tool_cfg.function.__name__)  # type: ignore
