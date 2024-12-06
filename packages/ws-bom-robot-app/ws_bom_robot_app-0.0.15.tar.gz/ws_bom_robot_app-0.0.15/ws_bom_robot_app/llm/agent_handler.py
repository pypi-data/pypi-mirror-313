from langchain_core.agents import AgentFinish
from langchain_core.outputs import ChatGenerationChunk, GenerationChunk
from langchain.callbacks.base import AsyncCallbackHandler
from ws_bom_robot_app.llm.utils.print import printJson, printString
from typing import Any, Dict, List, Optional, Union
from uuid import UUID
import ws_bom_robot_app.llm.settings as settings
from langchain_core.callbacks.base import AsyncCallbackHandler
from langchain_core.outputs import ChatGenerationChunk, GenerationChunk
from langchain_core.messages import BaseMessage, HumanMessage, AIMessage
import json

# Here is a custom handler that will print the tokens to stdout.
# Instead of printing to stdout you can send the data elsewhere; e.g., to a streaming API response


class AgentHandler(AsyncCallbackHandler):

    def __init__(self, threadId) -> None:
        super().__init__()
        self._threadId = threadId
        self.json_cards = None
        self.json_block = ""
        self.is_json_block = False
        self.backtick_count = 0  # Conteggio dei backticks per il controllo accurato

    async def on_llm_start(
        self,
        serialized: Dict[str, Any],
        prompts: List[str],
        *,
        run_id: UUID,
        parent_run_id: UUID = None,
        tags: List[str] = None,
        metadata: Dict[str, Any] = None,
        **kwargs: Any,
    ) -> None:
        firstChunk = {
            "type": "info",
            "threadId": self._threadId,
        }
        printJson(firstChunk)

    """async def on_chat_model_start(self, serialized: Dict[str, Any], messages: List[List[BaseMessage]], *, run_id: UUID = None, parent_run_id = None, tags = None, metadata = None, **kwargs: Any) -> Any:
        pass"""

    async def on_tool_end(self, output: Any, *, run_id: UUID, parent_run_id: UUID = None, tags: List[str] = None, **kwargs: Any) -> None:
      pass

    async def on_llm_new_token(
        self,
        token: str,
        *,
        chunk: Optional[Union[GenerationChunk, ChatGenerationChunk]] = None,
        run_id: UUID,
        parent_run_id: Optional[UUID] = None,
        tags: Optional[List[str]] = None,
        **kwargs: Any,
    ) -> None:
        """Gestisce i nuovi token durante lo streaming."""

        if token != "":
            self.backtick_count += token.count("`")

            if self.backtick_count >= 3:
                if not self.is_json_block:
                    self.is_json_block = True
                    self.json_block = ""
                else:
                    self.is_json_block = False
                    self.json_block += token.replace("```json", '')
                    await self.process_json_block(self.json_block)
                    self.json_block = ""
                self.backtick_count = 0
            elif self.is_json_block:
                self.json_block += token
            else:
                printString(token)
        pass

    async def on_agent_finish(
        self,
        finish: AgentFinish,
        *,
        run_id: UUID,
        parent_run_id: UUID = None,
        tags: List[str] = None,
        **kwargs: Any,
    ) -> None:
        settings.chat_history.extend(
            [
                AIMessage(content=finish.return_values["output"]),
            ]
        )
        if self.json_cards:
          for card in self.json_cards:
            printJson(card)
          self.json_cards = None
        finalChunk = {"type": "end"}
        printJson(finalChunk)

    async def process_json_block(self, json_block: str):
      """Processa il blocco JSON completo."""
      # Rimuove il delimitatore iniziale '```json' se presente, e spazi vuoti
      json_block_clean = json_block.replace('```', '').replace('json', '').strip()
      # Verifica che il blocco non sia vuoto prima di tentare il parsing
      if json_block_clean:
          try:
              # Prova a fare il parsing del JSON
              parsed_json = json.loads(json_block_clean)
              printJson(parsed_json)
          except json.JSONDecodeError as e:
              # Se il JSON è malformato, logga l'errore
              raise e

class RawAgentHandler(AsyncCallbackHandler):

    def __init__(self) -> None:
        super().__init__()

    async def on_llm_start(
        self,
        serialized: Dict[str, Any],
        prompts: List[str],
        *,
        run_id: UUID,
        parent_run_id: UUID = None,
        tags: List[str] = None,
        metadata: Dict[str, Any] = None,
        **kwargs: Any,
    ) -> None:
        pass

    """async def on_chat_model_start(self, serialized: Dict[str, Any], messages: List[List[BaseMessage]], *, run_id: UUID = None, parent_run_id = None, tags = None, metadata = None, **kwargs: Any) -> Any:
        pass"""

    async def on_tool_end(self, output: Any, *, run_id: UUID, parent_run_id: UUID = None, tags: List[str] = None, **kwargs: Any) -> None:
      pass

    async def on_llm_new_token(
        self,
        token: str,
        *,
        chunk: Optional[Union[GenerationChunk, ChatGenerationChunk]] = None,
        run_id: UUID,
        parent_run_id: Optional[UUID] = None,
        tags: Optional[List[str]] = None,
        **kwargs: Any,
    ) -> None:
        """Gestisce i nuovi token durante lo streaming."""
        if token != "":
            print(token)
        pass

    async def on_agent_finish(
        self,
        finish: AgentFinish,
        *,
        run_id: UUID,
        parent_run_id: UUID = None,
        tags: List[str] = None,
        **kwargs: Any,
    ) -> None:
        settings.chat_history.extend(
            [
                AIMessage(content=finish.return_values["output"]),
            ]
        )
