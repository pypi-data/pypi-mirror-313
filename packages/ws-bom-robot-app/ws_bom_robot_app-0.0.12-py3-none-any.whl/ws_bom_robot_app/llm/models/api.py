from typing import List, Dict, Optional, Union
from datetime import datetime
from pydantic import AliasChoices, BaseModel, Field, ConfigDict
from ws_bom_robot_app.llm.models.kb import LlmKbEndpoint, LlmKbIntegration
from ws_bom_robot_app.llm.utils.download import download_file
import os, shutil
from ws_bom_robot_app.config import Settings, config

class LlmMessage(BaseModel):
  role: str
  content: str

class LlmSearchSettings(BaseModel):
  search_type: Optional[str] = Field('default', validation_alias=AliasChoices("searchType","search_type"))
  score_threshold_id: Optional[float] = Field(None, validation_alias=AliasChoices("scoreThresholdId","score_threshold_id"))
  search_k: Optional[int] = Field(None, validation_alias=AliasChoices("searchK","search_k"))

class LlmRules(BaseModel):
  vector_db: Optional[str] = Field(None, validation_alias=AliasChoices("rulesVectorDb","vector_db"))
  threshold: Optional[float] = 0.7

class LlmAppToolChainSettings(BaseModel):
  prompt: Optional[str] = None
  model: Optional[str] = None
  temperature: int

class LlmAppToolDbSettings(BaseModel):
  connection_string: Optional[str] = Field(None, validation_alias=AliasChoices("connectionString","connection_string"))

class LlmAppTool(BaseModel):
  id: Optional[str] = None
  name: str
  description: Optional[str] = None
  type: str
  function_id: str = Field(..., validation_alias=AliasChoices("functionId","function_id"))
  function_name: str = Field(..., validation_alias=AliasChoices("functionName","function_name"))
  function_description: str = Field(..., validation_alias=AliasChoices("functionDescription","function_description"))
  model: Optional[str] = None
  secrets: Optional[List[Dict[str,str]]] = []
  llm_chain_settings: LlmAppToolChainSettings = Field(None, validation_alias=AliasChoices("llmChainSettings","llm_chain_settings"))
  data_source: str = Field(..., validation_alias=AliasChoices("dataSource","data_source"))
  db_settings: Optional[LlmAppToolDbSettings] = Field(None, validation_alias=AliasChoices("dbSettings","db_settings"))
  search_settings: LlmSearchSettings = Field(None, validation_alias=AliasChoices("searchSettings","search_settings"))
  integrations: Optional[List[LlmKbIntegration]] = None
  endpoints: Optional[List[LlmKbEndpoint]] = Field(None, validation_alias=AliasChoices("externalEndpoints","endpoints"))
  waiting_message: Optional[str] = Field("", validation_alias=AliasChoices("waitingMessage","waiting_message"))
  vector_db: Optional[str] = Field(None, validation_alias=AliasChoices("vectorDbFile","vector_db"))
  is_active: Optional[bool] = Field(True, validation_alias=AliasChoices("isActive","is_active"))
  model_config = ConfigDict(
      extra='allow'
  )

#region llm public endpoints

#region api
class LlmApp(BaseModel):
  system_message: str = Field(..., validation_alias=AliasChoices("systemMessage","system_message"))
  messages: List[LlmMessage]
  model: Optional[str] = None
  temperature: Optional[int] = 0
  secrets: Dict[str, str]
  app_tools: Optional[List[LlmAppTool]] = Field([], validation_alias=AliasChoices("appTools","app_tools"))
  vector_db: Optional[str] = Field(None, validation_alias=AliasChoices("vectorDb","vector_db"))
  rules: Optional[LlmRules] = None
  fine_tuned_model: Optional[str] = Field(None, validation_alias=AliasChoices("fineTunedModel","fine_tuned_model"))
  lang_chain_tracing: Optional[bool] = Field(False, validation_alias=AliasChoices("langChainTracing","lang_chain_tracing"))
  lang_chain_project: Optional[str] = Field(None, validation_alias=AliasChoices("langChainProject","lang_chain_project"))
  model_config = ConfigDict(
      extra='allow'
  )
  def __vector_db_folder(self) -> str:
    return os.path.join(config.robot_data_folder,config.robot_data_db_folder,config.robot_data_db_folder_store)
  def __vector_dbs(self):
      return list(set(
          os.path.basename(db) for db in [self.vector_db] +
          ([self.rules.vector_db] if self.rules and self.rules.vector_db else []) +
          [db for tool in (self.app_tools or []) for db in [tool.vector_db]]
          if db is not None
      ))
  def __decompress_zip(self,zip_file_path, extract_to):
    shutil.unpack_archive(zip_file_path, extract_to, "zip")
    os.remove(zip_file_path)
  async def __extract_db(self) -> None:
    for db_file in self.__vector_dbs():
      db_folder = os.path.join(self.__vector_db_folder(), os.path.splitext(db_file)[0])
      if not os.path.exists(db_folder):
        db_destination_file = os.path.join(db_folder, db_file)
        result: Optional[str] = await download_file(f'{config.robot_cms_host}/{config.robot_cms_db_folder}/' + db_file,db_destination_file, authorization=config.robot_cms_auth)
        if result:
          self.__decompress_zip(db_destination_file, db_folder)
        else:
          os.removedirs(db_folder)
  def __update_envs(self) -> None:
    _envs =  {
          "LANGCHAIN_API_KEY": self.secrets.get("langChainApiKey", ""),
          "LANGCHAIN_PROJECT": self.lang_chain_project or "",
          "LANGCHAIN_TRACING_V2": str(self.lang_chain_tracing).lower(),
          "NEBULY_API_KEY": self.secrets.get("nebulyApiKey", "")
      }
    os.environ.update({k: v for k, v in _envs.items() if v})
  def __normalize_vector_db_path(self) -> None:
    _vector_db_folder = self.__vector_db_folder()
    self.vector_db = os.path.join(_vector_db_folder, os.path.splitext(os.path.basename(self.vector_db))[0]) if self.vector_db else None
    if self.rules:
      self.rules.vector_db = os.path.join(_vector_db_folder, os.path.splitext(os.path.basename(self.rules.vector_db))[0]) if self.rules.vector_db else ""
    for tool in self.app_tools or []:
      tool.vector_db = os.path.join(_vector_db_folder, os.path.splitext(os.path.basename(tool.vector_db))[0]) if tool.vector_db else None
  async def initialize(self) -> None:
      self.__update_envs()
      await self.__extract_db()
      self.__normalize_vector_db_path()

class InvokeRequest(LlmApp):
  mode: str

class StreamRequest(LlmApp):
  thread_id: Optional[str] = Field(None, validation_alias=AliasChoices("threadId","thread_id"))
#endregion

#region vector_db
class VectorDbRequest(BaseModel):
  secrets: Optional[Dict[str, str]] = None
  def config(self) -> Settings:
    return config
  def api_key(self):
    return self.secrets.get("openAIApiKey", "")
  def out_name(self):
    return f"db_{datetime.now().strftime("%Y-%m-%d_%H-%M-%S-%f")[:-3]}_{os.getpid()}"

class RulesRequest(VectorDbRequest):
  type: Optional[str] = 'rules'
  rules: List[str]

class KbRequest(VectorDbRequest):
  files: Optional[List[str]] = []
  integrations: Optional[List[LlmKbIntegration]] = []
  endpoints: Optional[List[LlmKbEndpoint]] = []

class VectorDbResponse(BaseModel):
  success: bool = True
  file: Optional[str] = None
  error: Optional[str] = None

#endregion

#endregion

