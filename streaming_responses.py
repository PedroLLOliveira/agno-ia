# importa funções utilizadas
from typing import Iterator
from agno.agent import Agent, RunResponseEvent
from agno.models.openai import OpenAIChat
from agno.utils.pprint import pprint_run_response

# carrega variaveis de api_key
from dotenv import load_dotenv
load_dotenv()

# inicia agente usando modelos da OpenAI
agent = Agent(model=OpenAIChat(id="gpt-4o-mini"))

# envia uma pergunta pro agente usando streaming como variavel para resposta
response_stream: Iterator[RunResponseEvent] = agent.run(
    "Conte-me uma história curta de 5 segundos sobre um robô",
    stream=True
)

# retorna resposta no console
pprint_run_response(response_stream, markdown=True)