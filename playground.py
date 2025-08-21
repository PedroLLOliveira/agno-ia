from agno.agent import Agent
from agno.models.openai import OpenAIChat
from agno.playground import Playground
from agno.storage.sqlite import SqliteStorage
from agno.tools.duckduckgo import DuckDuckGoTools
from agno.tools.reasoning import ReasoningTools
from agno.knowledge.markdown import MarkdownKnowledgeBase
from agno.vectordb.lancedb import LanceDb, SearchType
from agno.embedder.openai import OpenAIEmbedder

# carrega variaveis de api_key
from dotenv import load_dotenv
load_dotenv()

# Banco local para histórico dos agentes
agent_storage: str = "tmp/agents.db"

# 1) Agente de Pesquisa Web
web_agent = Agent(
    name="Career Web Agent",
    model=OpenAIChat(id="gpt-4o"),
    tools=[DuckDuckGoTools()],
    instructions=[
        "Pesquise carreiras, salários (globais e no país do usuário, quando possível), "
        "pré-requisitos acadêmicos, certificações, trilhas de estudo e perspectivas futuras.",
        "Sempre inclua fontes confiáveis ao final (nome do site + URL).",
        "Se houver controvérsia ou variação regional, deixe isso claro."
    ],
    storage=SqliteStorage(table_name="career_web_agent", db_file=agent_storage),
    add_datetime_to_instructions=True,
    add_history_to_messages=True,
    num_history_responses=5,
    markdown=True,
)

# 2) Agente de Análise Vocacional
vocational_analyst = Agent(
    name="Vocational Analyst Agent",
    model=OpenAIChat(id="gpt-4o"),
    tools=[ReasoningTools(add_instructions=True)],
    instructions=[
        "Receber do usuário: interesses, habilidades, valores de trabalho, experiências e restrições (ex.: tempo, orçamento).",
        "Mapear o perfil para RIASEC (Realistic, Investigative, Artistic, Social, Enterprising, Conventional).",
        "Identificar top 3 áreas de afinidade e justificar com base nos sinais fornecidos pelo usuário.",
        "Gerar uma tabela com: Carreira | Por que combina | Passos de curto prazo (30-60 dias) | Recursos para aprender.",
        "Sugerir 3-5 trilhas de estudo (gratuitas e pagas), com carga horária estimada e ordem sugerida.",
        "Listar riscos/pressupostos (ex.: saturação de mercado, necessidade de portfolio).",
        "Quando possível, peça ao usuário para o Web Agent buscar dados adicionais (salários, demanda, certificações), "
        "e depois incorpore as fontes na análise final, citando-as."
    ],
    storage=SqliteStorage(table_name="vocational_analyst", db_file=agent_storage),
    add_datetime_to_instructions=True,
    add_history_to_messages=True,
    num_history_responses=5,
    markdown=True,
)

markdown_kb = MarkdownKnowledgeBase(
    path="./knowledge_base.md",
    vector_db=LanceDb(
        uri="tmp/lancedb",
        table_name="local_md_docs",
        search_type=SearchType.hybrid,
        embedder=OpenAIEmbedder(
            id="text-embedding-3-small",
            dimensions=1536,
        ),
    ),
)

docs_agent = Agent(
    name="Docs Agent",
    model=OpenAIChat(id="gpt-4o"),
    knowledge=markdown_kb,
    search_knowledge=True,
    instructions=[
        "Responda sempre com base na documentação local.",
        "Cite o arquivo markdown usado como fonte.",
        "Se não encontrar nada relevante, oriente o usuário a consultar o Web Agent."
    ],
    storage=SqliteStorage(table_name="docs_agent", db_file=agent_storage),
    add_datetime_to_instructions=True,
    add_history_to_messages=True,
    num_history_responses=5,
    markdown=True,
)

playground_app = Playground(agents=[web_agent, vocational_analyst, docs_agent])
app = playground_app.get_app()

if __name__ == "__main__":
    docs_agent.knowledge.load(recreate=False)
    playground_app.serve("playground:app", reload=True)
