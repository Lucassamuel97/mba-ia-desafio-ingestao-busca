# Ingestao e Busca Semantica com LangChain e Postgres

## Objetivo
Voce deve entregar um software capaz de:

- **Ingestao**: ler um arquivo PDF e salvar suas informacoes em um banco de dados PostgreSQL com extensao pgVector.
- **Busca**: permitir que o usuario faca perguntas via linha de comando (CLI) e receba respostas baseadas apenas no conteudo do PDF.

## Exemplo no CLI
Faça sua pergunta:

```
PERGUNTA: Qual o faturamento da Empresa SuperTechIABrazil?
RESPOSTA: O faturamento foi de 10 milhoes de reais.
```

Perguntas fora do contexto:

```
PERGUNTA: Quantos clientes temos em 2024?
RESPOSTA: Nao tenho informacoes necessarias para responder sua pergunta.
```

## Tecnologias obrigatorias
- Linguagem: Python
- Framework: LangChain
- Banco de dados: PostgreSQL + pgVector
- Execucao do banco de dados: Docker e Docker Compose (docker-compose fornecido no repositorio de exemplo)

## Pacotes recomendados
- Split: `from langchain_text_splitters import RecursiveCharacterTextSplitter`
- Embeddings (OpenAI): `from langchain_openai import OpenAIEmbeddings`
- Embeddings (Gemini): `from langchain_google_genai import GoogleGenerativeAIEmbeddings`
- PDF: `from langchain_community.document_loaders import PyPDFLoader`
- Ingestao: `from langchain_postgres import PGVector`
- Busca: `similarity_search_with_score(query, k=10)`

## OpenAI
- Crie uma API Key da OpenAI.
- Modelo de embeddings: `text-embedding-3-small`
- Modelo de LLM para responder: `gpt-5-nano`

## Gemini
- Crie uma API Key da Google.
- Modelo de embeddings: `models/embedding-001`
- Sugestao de modelo de LLM para responder: `gemini-2.5-flash-lite` ou `gemini-3.1-flash-lite-preview`.
- Voce pode utilizar outro modelo do Gemini de sua preferencia, desde que atinja os resultados esperados.
- Os limites de requisicoes gratuitas dos modelos podem mudar com frequencia. Para informacoes atualizadas, consulte a documentacao oficial do Google.

## Requisitos
### 1. Ingestao do PDF
- O PDF deve ser dividido em chunks de 1000 caracteres com overlap de 150.
- Cada chunk deve ser convertido em embedding.
- Os vetores devem ser armazenados no banco de dados PostgreSQL com pgVector.

### 2. Consulta via CLI
Criar um script Python para simular um chat no terminal.

Passos ao receber uma pergunta:

1. Vetorizar a pergunta.
2. Buscar os 10 resultados mais relevantes (k=10) no banco vetorial.
3. Montar o prompt e chamar a LLM.
4. Retornar a resposta ao usuario.

Prompt a ser utilizado:

```
CONTEXTO:
{resultados concatenados do banco de dados}

REGRAS:
- Responda somente com base no CONTEXTO.
- Se a informacao nao estiver explicitamente no CONTEXTO, responda:
  "Nao tenho informacoes necessarias para responder sua pergunta."
- Nunca invente ou use conhecimento externo.
- Nunca produza opinioes ou interpretacoes alem do que esta escrito.

EXEMPLOS DE PERGUNTAS FORA DO CONTEXTO:
Pergunta: "Qual e a capital da Franca?"
Resposta: "Nao tenho informacoes necessarias para responder sua pergunta."

Pergunta: "Quantos clientes temos em 2024?"
Resposta: "Nao tenho informacoes necessarias para responder sua pergunta."

Pergunta: "Voce acha isso bom ou ruim?"
Resposta: "Nao tenho informacoes necessarias para responder sua pergunta."

PERGUNTA DO USUARIO:
{pergunta do usuario}

RESPONDA A "PERGUNTA DO USUARIO"
```

## Estrutura obrigatoria do projeto
Faca um fork do repositorio para utilizar a estrutura abaixo: Clique aqui

```
├── docker-compose.yml
├── requirements.txt      # Dependencias
├── .env.example          # Template da variavel OPENAI_API_KEY
├── src/
│   ├── ingest.py         # Script de ingestao do PDF
│   ├── search.py         # Script de busca
│   ├── chat.py           # CLI para interacao com usuario
├── document.pdf          # PDF para ingestao
└── README.md             # Instrucoes de execucao
```

## Repositorios uteis
- Curso de nivelamento com LangChain
- Template basico com estrutura do projeto
- VirtualEnv para Python

Crie e ative um ambiente virtual antes de instalar dependencias:

```
python3 -m venv venv
source venv/bin/activate
```

## Ordem de execucao
1. Subir o banco de dados:

```
docker compose up -d
```

2. Executar ingestao do PDF:

```
python src/ingest.py
```

3. Rodar o chat:

```
python src/chat.py
```

## Entregavel
Repositorio publico no GitHub contendo todo o codigo-fonte e README com instrucoes claras de execucao do projeto.
