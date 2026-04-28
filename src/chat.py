import os
import sys

from search import TEST_QUESTION, search_prompt


HELP_TEXT = """
Comandos disponiveis:
    /help       Mostrar esta ajuda
    /exit       Sair do chat
    /quit       Sair do chat
    /clear      Limpar a tela
    /status     Verificar status do chat
    /test       Executar pergunta de teste
""".strip()

BANNER_LINES = [
"░█████╗░██╗░░██╗░█████╗░████████╗  ██████╗░░█████╗░░██████╗░",
"██╔══██╗██║░░██║██╔══██╗╚══██╔══╝  ██╔══██╗██╔══██╗██╔════╝░",
"██║░░╚═╝███████║███████║░░░██║░░░  ██████╔╝███████║██║░░██╗░",
"██║░░██╗██╔══██║██╔══██║░░░██║░░░  ██╔══██╗██╔══██║██║░░╚██╗",
"╚█████╔╝██║░░██║██║░░██║░░░██║░░░  ██║░░██║██║░░██║╚██████╔╝",
"░╚════╝░╚═╝░░╚═╝╚═╝░░╚═╝░░░╚═╝░░░  ╚═╝░░╚═╝╚═╝░░╚═╝░╚═════╝░",
]

DIVIDER = "=" * 60
SUBDIVIDER = "-" * 60

COLOR_RESET = "\033[0m"
COLOR_DIM = "\033[2m"
COLOR_BOLD = "\033[1m"
COLOR_CYAN = "\033[36m"
COLOR_GREEN = "\033[32m"
COLOR_YELLOW = "\033[33m"
COLOR_RED = "\033[31m"


def _supports_color():
    return sys.stdout.isatty() and os.getenv("TERM") not in (None, "dumb")


def _c(text, color):
    if not _supports_color():
        return text
    return f"{color}{text}{COLOR_RESET}"


def _clear_screen():
    os.system("cls" if os.name == "nt" else "clear")


def _print_banner():
    for line in BANNER_LINES:
        print(_c(line, COLOR_CYAN))
    print(_c(DIVIDER, COLOR_DIM))
    print(_c("Chat RAG - PDF -  Google Gemini + LangChain + pgVector", COLOR_BOLD))
    print("Digite sua pergunta ou /help para ver comandos.")
    print(_c(SUBDIVIDER, COLOR_DIM))


def _print_status():
    print(_c("Status:", COLOR_BOLD), _c("pronto para responder.", COLOR_GREEN))


def _print_error(message):
    print(_c("Erro:", COLOR_RED), message)


def _print_answer(answer):
    print(_c("RESPOSTA", COLOR_BOLD))
    print(_c(SUBDIVIDER, COLOR_DIM))
    print(_c(answer, COLOR_GREEN))
    print(_c(SUBDIVIDER, COLOR_DIM))


def _print_question(question):
    print(_c("PERGUNTA", COLOR_BOLD))
    print(_c(SUBDIVIDER, COLOR_DIM))
    print(question)

def main():
    chain = search_prompt()

    if not chain:
        _print_error("Não foi possível iniciar o chat. Verifique os erros de inicialização.")
        return
    
    _print_banner()

    while True:
        try:
            question = input(_c("➜ ", COLOR_GREEN) + _c("Pergunta", COLOR_BOLD) + ": ").strip()
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
                print(_c(HELP_TEXT, COLOR_DIM))
                continue
            if cmd == "/clear":
                _clear_screen()
                _print_banner()
                continue
            if cmd == "/status":
                _print_status()
                continue
            if cmd == "/test":
                try:
                    answer = chain(TEST_QUESTION)
                    _print_question(TEST_QUESTION)
                    _print_answer(answer)
                except Exception as exc:
                    _print_error(f"Erro ao responder: {exc}")
                continue

            print(_c("Comando desconhecido. Use /help para ver a lista.", COLOR_YELLOW))
            continue

        try:
            answer = chain(question)
            _print_answer(answer)
        except Exception as exc:
            _print_error(f"Erro ao responder: {exc}")

if __name__ == "__main__":
    main()