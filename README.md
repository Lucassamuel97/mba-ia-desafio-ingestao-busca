# Desafio MBA Engenharia de Software com IA - Full Cycle

## Requisitos

- Python 3.10+
- Docker e Docker Compose
- Chave da API do Google (Gemini)

## Configuracao

1) Copie o arquivo de exemplo:

```bash
cp .env.example .env
```

2) Edite o `.env` e informe a sua chave:

```
GOOGLE_API_KEY=SEU_TOKEN_AQUI
```

## Subir o banco

```bash
docker compose up -d
```

## Instalar dependencias

```bash
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
```

## Ingestao do PDF

```bash
python src/ingest.py
```

## Busca rapida (teste)

```bash
python src/search.py
```

## Chat interativo

```bash
python src/chat.py
```