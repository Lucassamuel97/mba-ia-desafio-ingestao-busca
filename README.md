# Desafio MBA Engenharia de Software com IA - Full Cycle

## Requisitos

- Docker e Docker Compose
- Chave da API do Google (Gemini)
- Make (opcional, mas recomendado para facilitar os comandos)

## Configuracao

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

## Ingestao do PDF

```bash
make ingest
```

## Busca rapida (teste)

```bash
make search
```

## Chat interativo

```bash
make chat
```