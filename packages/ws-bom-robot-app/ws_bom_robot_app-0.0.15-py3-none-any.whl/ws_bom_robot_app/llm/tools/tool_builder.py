from langchain.tools import StructuredTool
from ws_bom_robot_app.llm.models.api import LlmAppTool
from ws_bom_robot_app.llm.tools.tool_manager import ToolManager

def get_structured_tools(tools: list[LlmAppTool], api_key:str, callbacks:list) -> list[StructuredTool]:
  _structured_tools :list[StructuredTool] = []
  for tool in [tool for tool in tools if tool.is_active]:
    if _tool_config := ToolManager._list.get(tool.function_name):
      _tool_instance = ToolManager(tool, api_key, callbacks)
      _structured_tool = StructuredTool.from_function(
        coroutine=_tool_instance.get_coroutine(),
        name=tool.function_id,
        description=tool.function_description,
        args_schema=_tool_config.model
      )
      _structured_tool.tags = [tool.function_id]
      _structured_tools.append(_structured_tool)
  return _structured_tools
