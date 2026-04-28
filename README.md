# Desafio MBA Engenharia de Software com IA - Full Cycle

## Requisitos

- Python 3.10+ instalado
- Docker e Docker Compose
- Chave da API do Google (Gemini)

## Configuracao

1) Copie o arquivo de exemplo e preencha a chave:

```bash
cp .env.example .env
```

2) Edite o `.env` e informe a sua chave:

```
GOOGLE_API_KEY=SEU_TOKEN_AQUI
```

## Executar com Makefile

1) Suba os servicos (cria o `.venv` e instala dependencias):

```bash
make up
```

2) Ingestao do PDF:

```bash
make ingest
```

3) Buscar:

```bash
make search
```

4) Chat:

```bash
make chat
```

5) Limpar banco:

```bash
make db_clear
```

6) Parar servicos:

```bash
make down
```