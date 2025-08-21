from agno.agent import Agent
from agno.models.openai import OpenAIChat
from agno.team.team import Team
from agno.tools.reasoning import ReasoningTools

# carrega variaveis de api_key
from dotenv import load_dotenv
load_dotenv()

# 1) Agente de Produto: transforma a ideia em PRD e user stories
spec_agent = Agent(
    name="Product Spec Agent",
    role="Converter uma ideia de feature em PRD enxuto com user stories e critérios de aceite",
    model=OpenAIChat(id="gpt-4.1"),
    tools=[ReasoningTools(add_instructions=True)],
    instructions=[
        "Produza um PRD objetivo com: contexto, problema, objetivos, escopo-in/out.",
        "Crie user stories no formato: Como <persona>, quero <ação> para <benefício>.",
        "Inclua critérios de aceite claros e mensuráveis (Given/When/Then).",
    ],
    add_datetime_to_instructions=True,
)

# 2) Agente de API: propõe contrato REST/GraphQL com exemplos
api_agent = Agent(
    name="API Design Agent",
    role="Desenhar API (OpenAPI YAML) e exemplos de request/response",
    model=OpenAIChat(id="gpt-4.1"),
    tools=[ReasoningTools(add_instructions=True)],
    instructions=[
        "Forneça um trecho OpenAPI 3.1 (YAML) com paths, schemas e status codes.",
        "Inclua exemplos JSON realistas e erros comuns (4xx/5xx).",
        "Se houver autenticação, descreva o esquema (ex: Bearer JWT).",
    ],
    add_datetime_to_instructions=True,
)


# 3) Time coordenado: unifica as entregas em um pacote final
delivery_team = Team(
    name="Product Delivery Team",
    mode="coordinate",
    model=OpenAIChat(id="gpt-4.1"),
    members=[spec_agent, api_agent],
    tools=[ReasoningTools(add_instructions=True)],
    instructions=[
        "Consolidar as saídas em um documento único, bem seccionado.",
        "Verificar consistência entre PRD, API e modelo de dados.",
        "Garantir rastreabilidade: cada user story deve ter critérios de aceite e testes correspondentes.",
    ],
    markdown=True,
    show_members_responses=True,          # opcional: ver contribuições dos agentes
    enable_agentic_context=True,
    add_datetime_to_instructions=True,
    success_criteria=(
        "Documento final contém PRD, OpenAPI coerente, DDL SQL, "
        "plano de testes traceável e riscos/assunções explícitos."
    ),
)

if __name__ == "__main__":
    delivery_team.print_response(
        """Feature: Agenda de consultas para telemedicina
        Contexto:
          - Dois perfis: Médico e Paciente.
          - Médico define janelas disponíveis; Paciente agenda dentro dessas janelas.
          - Confirmação via e-mail/SMS; reagendamento e cancelamento com política de 24h.
          - Integração futura com sala ACS (não implementar agora).
        Requisitos:
          1) PRD com user stories e critérios de aceite (Given/When/Then).
          2) Contrato de API (OpenAPI YAML) para: criar disponibilidade, listar slots, criar/cancelar/reagendar consulta.
          3) DDL SQL (PostgreSQL) com tabelas: doctors, patients, availabilities, appointments, notifications.
          4) Plano de testes (unit/integration/e2e) mapeado para os critérios de aceite.
          5) Riscos, assunções e métricas de sucesso (ex: taxa de no-show, lead time de agendamento).
        """,
        stream=True,
        show_full_reasoning=True,
        stream_intermediate_steps=True,
    )
