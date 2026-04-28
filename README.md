# Desafio MBA Engenharia de Software com IA - Full Cycle

Projeto de ingestão e busca semântica em PDF usando LangChain e PostgreSQL com pgVector.
O objetivo completo do desafio está em [desafio.md](desafio.md).

## O que a aplicação faz

- Lê um PDF, divide o texto em chunks, gera embeddings e salva no PostgreSQL.
- Permite perguntar via CLI e responde somente com base no conteúdo ingerido.
- Se a informação não estiver no PDF, responde com uma mensagem padrão.

## Exemplos de perguntas

- Qual o faturamento da Empresa SuperTechIABrazil?
- Qual o nome do diretor financeiro citado no documento?
- Qual é a capital da França? (fora do contexto, deve recusar)

## Arquitetura

- `src/ingest.py`: carrega o PDF, faz split, gera embeddings e grava no pgVector.
- `src/search.py`: busca similaridade no banco para validar o pipeline.
- `src/chat.py`: CLI interativo que monta o prompt e consulta o LLM.
- PostgreSQL + pgVector rodando via Docker Compose.

## Requisitos

- Docker e Docker Compose
- Chave da API do Google (Gemini)
- Make (opcional, mas recomendado para facilitar os comandos)

## Configuração

1) Copie o arquivo de exemplo:

```bash
cp .env.example .env
```

2) Edite o `.env` e informe a sua chave:

```
GOOGLE_API_KEY=SEU_TOKEN_AQUI
```

## Subir tudo (banco + app)

```bash
make up
```

## Ingestão do PDF

```bash
make ingest
```

## Busca rápida (teste)

```bash
make search
```

## Chat interativo (CLI)

```bash
make chat
```