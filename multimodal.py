# importa funções utilizadas
from agno.agent import Agent
from agno.media import Image
from agno.models.openai import OpenAIChat
from agno.tools.duckduckgo import DuckDuckGoTools

# carrega variaveis de api_key
from dotenv import load_dotenv
load_dotenv()

# inicia agente usando modelos da OpenAI passando ferramentas como parametros
agent = Agent(
    model=OpenAIChat(id="gpt-4o"),
    tools=[DuckDuckGoTools()],
    markdown=True,
)

# envia uma pergunta pro agente passando um link para analise de imagem
agent.print_response(
    "Quais soluções a rubeus oferece?",
    images=[
        Image(
            url="https://imgs.search.brave.com/YI9alEm_bxktdkjB4lqS13VwCsDgBM5olKU_WrOOxl4/rs:fit:860:0:0:0/g:ce/aHR0cHM6Ly9ydWJl/dXMuY29tLmJyL3dw/LWNvbnRlbnQvdXBs/b2Fkcy8yMDI0LzEx/L2FuYWxpc3RhLXJ1/YmV1cy1lc3BlY2lh/bGlzdGEtZW0tdG90/dnMud2VicA"
        )
    ],
    stream=True,
)