# importa funções utilizadas
from agno.agent import Agent, RunResponse
from agno.models.openai import OpenAIChat
from agno.utils.pprint import pprint_run_response

# carrega variaveis de api_key
from dotenv import load_dotenv
load_dotenv()

# inicia agente usando modelos da OpenAI
agent = Agent(model=OpenAIChat(id="gpt-4o-mini"))

# envia uma pergunta pro agente
response: RunResponse = agent.run("Conte-me uma história curta de 5 segundos sobre um robô")

# retorna resposta no console
pprint_run_response(response, markdown=True)