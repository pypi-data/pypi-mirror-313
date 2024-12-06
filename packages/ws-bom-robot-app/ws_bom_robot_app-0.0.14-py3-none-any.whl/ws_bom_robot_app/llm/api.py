import openai
from typing import Annotated
from fastapi import APIRouter, HTTPException, Header
from fastapi.responses import StreamingResponse
from ws_bom_robot_app.llm.agent_description import AgentDescriptor
from ws_bom_robot_app.llm.models.api import InvokeRequest, StreamRequest, RulesRequest, KbRequest, VectorDbResponse
from ws_bom_robot_app.llm.main import invoke, stream, stream_none
from ws_bom_robot_app.llm.models.base import IdentifiableEntity
from ws_bom_robot_app.llm.vector_store.generator import kb, rules, kb_stream_file
from ws_bom_robot_app.llm.tools.tool_manager import ToolManager
from ws_bom_robot_app.llm.vector_store.integration.manager import IntegrationManager
from ws_bom_robot_app.task_manager import task_manager, TaskHeader

router = APIRouter(prefix="/api/llm", tags=["llm"])

@router.get("/")
async def root():
    return {}

@router.post("/invoke")
async def _invoke(rq: InvokeRequest):
    return await invoke(rq)

@router.post("/stream")
async def _stream(rq: StreamRequest) -> StreamingResponse:
    return StreamingResponse(stream(rq), media_type="application/json")

@router.post("/stream/none")
async def _stream_none(rq: StreamRequest) -> None:
    await stream_none(rq)

@router.post("/stream/raw")
async def _stream_raw(rq: StreamRequest) -> StreamingResponse:
    return StreamingResponse(stream(rq, formatted=False), media_type="application/json")

@router.post("/stream/raw/none")
async def _stream_raw_none(rq: StreamRequest) -> None:
     await stream_none(rq, formatted=False)

@router.post("/kb")
async def _kb(rq: KbRequest) -> VectorDbResponse:
    return await kb(rq)

@router.post("/kb/task")
async def _kb_task(rq: KbRequest, headers: Annotated[TaskHeader, Header()]) -> IdentifiableEntity:
    return task_manager.create_task(kb(rq),headers)

@router.post("/rules")
async def _rules(rq: RulesRequest) -> VectorDbResponse:
    return await rules(rq)

@router.post("/rules/task")
async def _rules_task(rq: RulesRequest, headers: Annotated[TaskHeader, Header()]) -> IdentifiableEntity:
    return task_manager.create_task(rules(rq),headers)

@router.get("/kb/file/{filename}")
async def _kb_get_file(filename: str) -> StreamingResponse:
    return await kb_stream_file(filename)

@router.get("/extension/tools", tags=["extension"])
def _extension_tools():
    return [{"id": key, "value": key} for key in ToolManager._list.keys()]
@router.get("/extension/agents", tags=["extension"])
def _extension_agents():
    return [{"id": key, "value": key} for key in AgentDescriptor._list.keys()]
@router.get("/extension/integrations", tags=["extension"])
def _extension_integrations():
    return [{"id": key, "value": key} for key in IntegrationManager._list.keys()]

@router.post("/openai/models")
def _openai_models(secrets: dict[str, str]):
    """_summary_
    Args:
        secrets: dict[str, str] with openAIApiKey key
    Returns:
        list: id,created,object,owned_by
    """
    if not "openAIApiKey" in secrets:
        raise HTTPException(status_code=401, detail="openAIApiKey not found in secrets")
    openai.api_key = secrets.get("openAIApiKey")
    response = openai.models.list()
    return response.data
