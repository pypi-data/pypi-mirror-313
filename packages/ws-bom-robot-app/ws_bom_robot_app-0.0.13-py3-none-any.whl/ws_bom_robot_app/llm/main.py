from typing import  AsyncGenerator
from ws_bom_robot_app.llm.agent_lcel import AgentLcel
from ws_bom_robot_app.llm.agent_handler import AgentHandler, RawAgentHandler
from ws_bom_robot_app.llm.agent_description import AgentDescriptor
from langchain_core.messages import HumanMessage, AIMessage
from ws_bom_robot_app.llm.tools.tool_builder import get_structured_tools
from ws_bom_robot_app.llm.models.api import InvokeRequest, StreamRequest
import ws_bom_robot_app.llm.settings as settings
from nebuly.providers.langchain import LangChainTrackingHandler
from langchain_core.callbacks.base import AsyncCallbackHandler
import warnings, asyncio, os, io, sys, json
from typing import List

async def invoke(rq: InvokeRequest) -> str:
  await rq.initialize()
  _msg: str = rq.messages[-1].content
  processor = AgentDescriptor(api_key=rq.secrets["openAIApiKey"],
      prompt=rq.system_message,
      mode = rq.mode,
      rules=rq.rules if rq.rules else None
  )
  result: AIMessage = await processor.run_agent(_msg)
  return {"result": result.content}

async def __stream(rq: StreamRequest,formatted: bool = True) -> None:
  await rq.initialize()
  callbacks: List[AsyncCallbackHandler] = [AgentHandler(rq.thread_id) if formatted else RawAgentHandler()]
  settings.init()

  #CREATION OF CHAT HISTORY FOR AGENT
  for message in rq.messages:
      if message.role == "user":
          settings.chat_history.append(HumanMessage(content=message.content))
      elif message.role == "assistant":
          message_content = ""
          if '{\"type\":\"string\"' in message.content:
            try:
              json_msg = json.loads('[' + message.content[:-1] + ']')
              for msg in json_msg:
                if msg.get("content"):
                  message_content += msg["content"]
            except:
              message_content = message.content
          else:
            message_content = message.content
          settings.chat_history.append(AIMessage(content=message_content))

  processor = AgentLcel(
      openai_config={"api_key": rq.secrets["openAIApiKey"], "openai_model": rq.model, "temperature": rq.temperature},
      sys_message=rq.system_message,
      tools=get_structured_tools(tools=rq.app_tools, api_key=rq.secrets["openAIApiKey"], callbacks=[callbacks[0]]),
      rules=rq.rules
  )

  if "NEBULY_API_KEY" in os.environ:
    nebuly_callback = LangChainTrackingHandler(
            api_key= os.environ["NEBULY_API_KEY"],
            user_id=rq.thread_id,
        )
    callbacks.append(nebuly_callback)

  with warnings.catch_warnings():
    warnings.simplefilter("ignore", UserWarning)
    await processor.executor.ainvoke(
        {"input": rq.messages[-1], "chat_history": settings.chat_history},
        {"callbacks": callbacks},
    )

async def stream(rq: StreamRequest,formatted:bool = True) -> AsyncGenerator[str, None]:
    sys_stdout = io.StringIO()
    original_stdout = sys.stdout
    sys.stdout = sys_stdout
    try:
        task = asyncio.create_task(__stream(rq,formatted))
        while not task.done():
            await asyncio.sleep(0.1)  # yield control to avoid blocking
            output = sys_stdout.getvalue()
            if output:
                yield output
                sys_stdout.truncate(0)
                sys_stdout.seek(0)
        # capture any remaining output after the task completes
        output = sys_stdout.getvalue()
        if output:
            yield output
    finally:
        sys.stdout = original_stdout

async def stream_none(rq: StreamRequest, formatted: bool = True) -> None:
  await __stream(rq, formatted)
