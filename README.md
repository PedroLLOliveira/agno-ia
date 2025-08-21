# Estudos sobre a Biblioteca AGNO AI

Testei varias formas de usar as funções de criação de agentes inteligentes disponibilizados pela biblioteca e documentei todos exemplos praticos nesse repositorio.

A seguir veremos como rodar cada exemplo ja adicionado ao repositorio, alem de como rodar a interface UI disponivel criada pelos devs que criaram e mantem a lib do AGNO.

---

## Criação do ambiente python
Para rodar todo o projeto deve seguir alguns passos para instalação.

### 1. Clonar o repositório
```bash
git clone https://github.com/seu-usuario/seu-projeto.git
cd seu-projeto
```
### 2. Criar o ambiente virtual python
- Linux/Mac
```bash
# Criar o venv
python3 -m venv .venv

# Ativar o venv
source .venv/bin/activate
```
- Windows
```bash
# Criar o venv
python -m venv .venv

# Ativar o venv
.\.venv\Scripts\Activate
```
### 3. Instalar o gerenciador uv
Dentro do ambiente ja ativado
- Linux/Mac/Windows
```bash
pip install uv
```
### 4. Instalar as dependencias
Ainda com o ambiente virtual ativado:
- Linux/Mac/Windows
```bash
uv pip install -r requirements.txt
```

--- 

## API KEYS
Para que o projeto funcione as integrações foi configurado para utilziar os modelos da openai em todos os exemplos. Para conseguir fazer uso você tem que possuir uma chave de api da openai com saldo de credito disponivel e adicionar a um arquivo .env.

- No arquivo .env adicione a seguinte variavel
```bash
OPENAI_API_KEY=sk-proj-....
```

## Exemplos criados (rodando no terminal)

- Agente simples: cria um agente que usa o modelo de inteligencia artifical da openai para responder as perguntas dos usuarios.
- Agente simples com resposta em streaming: cria um agente simples mas usa a resposta em streaming no terminal.
- Agente muiltimodal: cria um agente que consegue analisar imagens e responder a pergunta de agora com o conteudo da imagem.
- Multi-agentes: cria um time de dois agentes que vao trocar informações entre si para gerar um plano de criação de produto a partir de um contexto fornecido pelo usuario.

### Como Rodar
Com o ambiente configurado e dependencias instaladas. 
Ative a venv e rode o comando python a seguir como nome do arquivo que você deseja testar o agente listado a cima.

```bash
python nome_do_arquivo.py
```

---

## Rodando com interface AGNO UI

A lib nos permite clonar um projeto UI frontend que tem uma plataforma pronta para conectar com os agentes que voce criou e testalos usando uma interface web.

Para rodar devemos seguir alguns passos:

### Rodar o arquivo do playground python
Na raiz do projeto com o venv ativado, no seu terminal execute o seguinte comando.
```bash
python playground.py
```

### Para rodar o AGNO UI
- Você deve navegar até a pasta frontend ja clonada no repositorio 
```bash
cd ui/agent-ui
```
- Ja dentro da pasta você deve instalar as dependencias do npm.
```bash
npm install
```
- Com as dependencias instaladas basta rodar o comando de executar o projeto.
```bash
npm run dev
```

- O agno ui vai estar disponivel em http://localhost:3000 ja configurado com os agentes locais do arquivo playground.py


