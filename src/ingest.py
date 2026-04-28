import os
import sys

from dotenv import load_dotenv
from langchain_community.document_loaders import PyPDFLoader
from langchain_google_genai import GoogleGenerativeAIEmbeddings
from langchain_postgres import PGVector
from langchain_text_splitters import RecursiveCharacterTextSplitter

load_dotenv()

def ingest_pdf():
    print("Iniciando processo de ingestao do PDF...")

    pdf_path = os.getenv("PDF_PATH")
    database_url = os.getenv("DATABASE_URL")
    collection_name = os.getenv("PG_VECTOR_COLLECTION_NAME")
    google_embedding_model = os.getenv("GOOGLE_EMBEDDING_MODEL", "text-embedding-004")

    try:
        if not pdf_path:
            raise ValueError("PDF_PATH nao configurado no .env")
        if not os.path.exists(pdf_path):
            raise FileNotFoundError(f"PDF nao encontrado em {pdf_path}")
        if not database_url:
            raise ValueError("DATABASE_URL nao configurado no .env")
        if not collection_name:
            raise ValueError("PG_VECTOR_COLLECTION_NAME nao configurado no .env")

        print(f"Carregando PDF: {pdf_path}")
        loader = PyPDFLoader(pdf_path)
        docs = loader.load()
        print(f"PDF carregado: {len(docs)} paginas")

        print("Dividindo texto em chunks...")
        splitter = RecursiveCharacterTextSplitter(
            chunk_size=1000,
            chunk_overlap=150,
            length_function=len,
            separators=["\n\n", "\n", " ", ""],
        )
        chunks = splitter.split_documents(docs)
        print(f"Texto dividido em {len(chunks)} chunks")

        print("Configurando embeddings do Google...")
        embeddings = GoogleGenerativeAIEmbeddings(model=google_embedding_model)

        print("Conectando ao banco de dados...")
        vectorstore = PGVector(
            embeddings=embeddings,
            collection_name=collection_name,
            connection=database_url,
            use_jsonb=True,
        )

        print("Salvando chunks no banco vetorial...")
        print("Isso pode demorar alguns minutos...")

        batch_size = 5
        total_batches = (len(chunks) - 1) // batch_size + 1

        for i in range(0, len(chunks), batch_size):
            batch = chunks[i : i + batch_size]
            vectorstore.add_documents(batch)

            current_batch = i // batch_size + 1
            print(f"Lote {current_batch}/{total_batches} salvo")

        print("Sucesso! Ingestao concluida.")
        print(f"Chunks salvos: {len(chunks)}")
        print(f"Colecao: {collection_name}")
        print(f"Banco: {database_url}")
    except Exception as exc:
        print(f"Erro durante a ingestao: {exc}")
        print("Verifique se:")
        print("- O banco PostgreSQL esta rodando (docker compose up -d)")
        print("- O GOOGLE_API_KEY esta correto no .env")
        print("- O arquivo PDF existe e e valido")
        sys.exit(1)


if __name__ == "__main__":
    ingest_pdf()