from typing import Any
from langchain.agents import AgentExecutor
from langchain_openai import ChatOpenAI
from langchain_core.prompts import ChatPromptTemplate, MessagesPlaceholder
from langchain.agents.format_scratchpad.openai_tools import (
    format_to_openai_tool_messages,
)
from langchain.agents.output_parsers.openai_tools import OpenAIToolsAgentOutputParser
from langchain_core.runnables import RunnableLambda
from datetime import datetime
from langchain_openai import OpenAIEmbeddings
from ws_bom_robot_app.llm.models.api import LlmMessage, LlmRules
from ws_bom_robot_app.llm.utils.agent_utils import get_rules
from ws_bom_robot_app.llm.defaut_prompt import default_prompt

class AgentLcel:

    def __init__(self, openai_config: dict, sys_message: str, tools: list, rules: LlmRules = None):
        self.__apy_key = openai_config["api_key"]
        self.sys_message = sys_message.format(
            date_stamp=datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
            lang="it",
        )
        self.__tools = tools
        self.rules = rules
        self.embeddings = OpenAIEmbeddings(api_key= self.__apy_key) # type: ignore
        self.memory_key = "chat_history"
        self.__llm = ChatOpenAI(
            api_key=self.__apy_key, # type: ignore
            model=openai_config["openai_model"],
            temperature=openai_config["temperature"],
            streaming=True,
        )
        self.__llm_with_tools = self.__llm.bind_tools(self.__tools) if len(self.__tools) > 0 else self.__llm
        self.executor = self.__create_agent()

    async def __create_prompt(self, input):
        message : LlmMessage = input["input"]
        input = message.content
        rules_prompt = await get_rules(self.rules,self.__apy_key, input) if self.rules else ""
        system = default_prompt + self.sys_message + rules_prompt
        return ChatPromptTemplate.from_messages(
            [
                (
                    "system", system
                ),
                MessagesPlaceholder(variable_name=self.memory_key),
                ("user", "{input}"),
                MessagesPlaceholder(variable_name="agent_scratchpad"),
            ]
        )

    def __create_agent(self):
      agent: Any = (
          {
            "input": lambda x: x["input"],
            "agent_scratchpad": lambda x: format_to_openai_tool_messages(x["intermediate_steps"]),
            "chat_history": lambda x: x["chat_history"],
          }
          | RunnableLambda(self.__create_prompt)
          | self.__llm_with_tools
          | OpenAIToolsAgentOutputParser()
      )
      return AgentExecutor(agent=agent, tools=self.__tools, verbose=False)
