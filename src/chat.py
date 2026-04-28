import os
import sys

from search import TEST_QUESTION, search_prompt


HELP_TEXT = """
Comandos disponiveis:
    /help      Mostrar esta ajuda
    /exit      Sair do chat
    /quit      Sair do chat
    /clear     Limpar a tela
    /status    Verificar status do chat
    /test      Executar pergunta de teste
""".strip()


def _clear_screen():
        os.system("cls" if os.name == "nt" else "clear")


def _print_banner():
        print("Chat RAG - PDF")
        print("Digite sua pergunta ou /help para ver comandos.")
        print("-")

def main():
    chain = search_prompt()

    if not chain:
        print("Não foi possível iniciar o chat. Verifique os erros de inicialização.")
        return
    
    _print_banner()

    while True:
        try:
            question = input("PERGUNTA: ").strip()
        except (EOFError, KeyboardInterrupt):
            print("\nEncerrando chat.")
            return

        if not question:
            continue

        if question.startswith("/"):
            cmd = question.lower()
            if cmd in ("/exit", "/quit"):
                print("Até mais.")
                return
            if cmd == "/help":
                print(HELP_TEXT)
                continue
            if cmd == "/clear":
                _clear_screen()
                _print_banner()
                continue
            if cmd == "/status":
                print("Status: pronto para responder.")
                continue
            if cmd == "/test":
                try:
                    answer = chain(TEST_QUESTION)
                    print(f"PERGUNTA: {TEST_QUESTION}")
                    print(f"RESPOSTA: {answer}")
                except Exception as exc:
                    print(f"Erro ao responder: {exc}")
                continue

            print("Comando desconhecido. Use /help para ver a lista.")
            continue

        try:
            answer = chain(question)
            print(f"RESPOSTA: {answer}")
        except Exception as exc:
            print(f"Erro ao responder: {exc}")

if __name__ == "__main__":
    main()