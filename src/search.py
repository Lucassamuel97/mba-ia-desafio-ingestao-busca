import os

from dotenv import load_dotenv
from langchain_google_genai import ChatGoogleGenerativeAI, GoogleGenerativeAIEmbeddings
from langchain_postgres import PGVector

load_dotenv()

PROMPT_TEMPLATE = """
CONTEXTO:
{contexto}

REGRAS:
- Responda somente com base no CONTEXTO.
- Se a informação não estiver explicitamente no CONTEXTO, responda:
  "Não tenho informações necessárias para responder sua pergunta."
- Nunca invente ou use conhecimento externo.
- Nunca produza opiniões ou interpretações além do que está escrito.

EXEMPLOS DE PERGUNTAS FORA DO CONTEXTO:
Pergunta: "Qual é a capital da França?"
Resposta: "Não tenho informações necessárias para responder sua pergunta."

Pergunta: "Quantos clientes temos em 2024?"
Resposta: "Não tenho informações necessárias para responder sua pergunta."

Pergunta: "Você acha isso bom ou ruim?"
Resposta: "Não tenho informações necessárias para responder sua pergunta."

PERGUNTA DO USUÁRIO:
{pergunta}

RESPONDA A "PERGUNTA DO USUÁRIO"
"""

DATABASE_URL = os.getenv("DATABASE_URL")
COLLECTION_NAME = os.getenv("PG_VECTOR_COLLECTION_NAME")
GOOGLE_EMBEDDING_MODEL = os.getenv("GOOGLE_EMBEDDING_MODEL", "text-embedding-004")
GOOGLE_LLM_MODEL = os.getenv("GOOGLE_LLM_MODEL", "gemini-2.5-flash-lite")
TEST_QUESTION = "Qual o faturamento da Empresa SuperTechIABrazil?"

def _build_context(results):
  parts = []
  for doc, score in results:
    parts.append(doc.page_content)
  return "\n\n".join(parts)


def search_prompt(question=None):
  if not DATABASE_URL:
    raise ValueError("DATABASE_URL nao configurado no .env")
  if not COLLECTION_NAME:
    raise ValueError("PG_VECTOR_COLLECTION_NAME nao configurado no .env")

  embeddings = GoogleGenerativeAIEmbeddings(model=GOOGLE_EMBEDDING_MODEL)
  store = PGVector(
    embeddings=embeddings,
    collection_name=COLLECTION_NAME,
    connection=DATABASE_URL,
    use_jsonb=True,
  )

  llm = ChatGoogleGenerativeAI(model=GOOGLE_LLM_MODEL, temperature=0)

  def answer(question_text):
    if not question_text:
      return ""
    results = store.similarity_search_with_score(question_text, k=10)
    context = _build_context(results)
    prompt = PROMPT_TEMPLATE.format(contexto=context, pergunta=question_text)
    response = llm.invoke(prompt)
    return getattr(response, "content", str(response))

  if question is not None:
    return answer(question)

  return answer


if __name__ == "__main__":
  print("Teste rapido de busca")
  result = search_prompt(TEST_QUESTION)
  print(f"PERGUNTA: {TEST_QUESTION}")
  print(f"RESPOSTA: {result}")