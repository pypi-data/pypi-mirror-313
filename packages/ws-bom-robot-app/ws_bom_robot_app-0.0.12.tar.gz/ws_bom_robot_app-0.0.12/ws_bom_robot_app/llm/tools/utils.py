import random
from langchain_openai import ChatOpenAI
from langchain_core.prompts import PromptTemplate
from ws_bom_robot_app.llm.utils.print import printString

def getRandomWaitingMessage(waiting_messages: str, traduction: bool = True) -> str:
  if not waiting_messages: return ""
  messages = [msg.strip() for msg in waiting_messages.split(";") if msg.strip()]
  if not messages: return ""
  chosen_message = random.choice(messages) + "\n"
  if not traduction:
      printString(chosen_message)
  return chosen_message

async def translate_text(api_key, language, text: str, callbacks: list) -> str:
  if language == "it":
      printString(text)
      return
  llm = ChatOpenAI(api_key=api_key, model="gpt-3.5-turbo-0125", streaming=True)
  sys_message = """Il tuo compito è di tradurre il testo_da_tradure nella seguente lingua: \n\n lingua: {language}\n\n testo_da_tradure: {testo_da_tradure} \n\nTraduci il testo_da_tradure nella lingua {language} senza aggiungere altro:"""
  prompt = PromptTemplate.from_template(sys_message)
  chain = prompt | llm
  await chain.ainvoke({"language":language, "testo_da_tradure": text}, {"callbacks": callbacks})
