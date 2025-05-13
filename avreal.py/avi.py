import json
import os
import random

arquivo_tudo = "inf.json"


def load_inf():
    try:
        if os.path.exists(arquivo_tudo):
            with open(arquivo_tudo, "r") as file:
                data = json.load(file)
            if "usuarios" not in data:
                data["usuarios"] = {}
            if "mensagens" not in data:
                data["mensagens"] = {}
            return data
        else:
            return {"usuarios": {}, "mensagens": {}}
    except Exception as e:
        print(f"Erro ao carregar arquivo: {e}")
        return {"usuarios": {}, "mensagens": {}}


def save_inf(inf):
    with open(arquivo_tudo, "w") as file:
        json.dump(inf, file, indent=4)


def gerar_id():
    return str(random.randint(1000, 9999))


def cadastrar_usuario(dados):
    nome = input("Digite seu nome: ")
    distrito = input("Digite seu distrito: ")
    user_id = gerar_id()
    if any(dados["usuarios"][uid]["nome"] == nome for uid in dados["usuarios"]):
        print("Nome já cadastrado.")
        return
    dados["usuarios"][user_id] = {
        "nome": nome,
        "distrito": distrito,
        "id": user_id
    }
    save_inf(dados)
    print(f"Usuário cadastrado com sucesso! Seu ID é: {user_id}")
    return user_id


def login(dados):
    nome = input("Digite seu nome: ")
    user_id = input("Digite seu ID (4 números): ")
    if not user_id.isdigit() or len(user_id) != 4:
        print("ID inválido. Por favor, digite 4 números.")
        return None
    for uid in dados["usuarios"]:
        if dados["usuarios"][uid]["nome"] == nome and dados["usuarios"][uid]["id"] == user_id:
            print("Login realizado com sucesso!")
            return uid
    print("Nome ou ID incorretos.")
    return None


def enviar_mensagem(remetente, dados):
    print("\nOpções de envio de mensagem:")
    print("1. Enviar para todos do meu distrito")
    print("2. Enviar para um usuário específico")
    opcao = input("Escolha uma opção: ")

    if opcao == "1":
        mensagem = input("Digite sua mensagem: ")
        destinatarios = [
            uid for uid, user in dados["usuarios"].items()
            if user["distrito"] == dados["usuarios"][remetente]["distrito"]
               and uid != remetente
        ]
        if not destinatarios:
            print("Você é o único usuário do seu distrito.")
            return
        for dest in destinatarios:
            if dest not in dados["mensagens"]:
                dados["mensagens"][dest] = []
            dados["mensagens"][dest].append(
                f"De {dados['usuarios'][remetente]['nome']} ({remetente}): {mensagem}"
            )
        save_inf(dados)
        print("Mensagem enviada para todos do seu distrito!")
    elif opcao == "2":
        destinatario_id = input("Digite o ID do destinatário (4 números): ")
        if not destinatario_id.isdigit() or len(destinatario_id) != 4:
            print("ID inválido. Por favor, digite 4 números.")
            return
        if destinatario_id not in dados["usuarios"]:
            print("Destinatário não encontrado.")
            return
        mensagem = input("Digite sua mensagem: ")
        if destinatario_id not in dados["mensagens"]:
            dados["mensagens"][destinatario_id] = []
        dados["mensagens"][destinatario_id].append(
            f"De {dados['usuarios'][remetente]['nome']} ({remetente}): {mensagem}"
        )
        save_inf(dados)
        print("Mensagem enviada com sucesso!")
    else:
        print("Opção inválida.")


def visualizar_mensagem(usuario, dados):
    print("=== Suas Mensagens ===")
    if usuario not in dados["mensagens"] or not dados["mensagens"][usuario]:
        print("Você não tem mensagens.")
    else:
        for i, msg in enumerate(dados["mensagens"][usuario], 1):
            print(f"{i}. {msg}")
    print()


def excluir_conta(arma, dados):
    if arma in dados["usuarios"]:
        del dados["usuarios"][arma]
        if arma in dados["mensagens"]:
            del dados["mensagens"][arma]
        save_inf(dados)
        print("Conta excluída com sucesso!")
    else:
        print("Usuário não encontrado.")


def ver_perfil(arma, dados):
    print(f"Nome: {dados['usuarios'][arma]['nome']}")
    print(f"Distrito: {dados['usuarios'][arma]['distrito']}")
    print(f"ID: {dados['usuarios'][arma]['id']}")


def menu_usuario(arma, dados):
    while True:
        print(f"\n=== Menu do Usuário: {dados['usuarios'][arma]['nome']} ===")
        print("1. Ver perfil")
        print("2. Enviar mensagem")
        print("3. Ver mensagens recebidas")
        print("4. Excluir conta")
        print("5. Voltar ao menu principal")
        opcao = input("Escolha uma opção: ")
        if opcao == "1":
            ver_perfil(arma, dados)
        elif opcao == "2":
            enviar_mensagem(arma, dados)
        elif opcao == "3":
            visualizar_mensagem(arma, dados)
        elif opcao == "4":
            excluir_conta(arma, dados)
            break
        elif opcao == "5":
            break
        else:
            print("Opção inválida. Por favor, escolha uma opção válida.")


def menu_principal(dados):
    while True:
        print("\n=== Menu Principal ===")
        print("1. Cadastrar usuário")
        print("2. Entrar no sistema")
        print("3. Sair")
        opcao = input("Escolha uma opção: ")
        if opcao == "1":
            cadastrar_usuario(dados)
        elif opcao == "2":
            arma = login(dados)
            if arma:
                menu_usuario(arma, dados)
        elif opcao == "3":
            print("Saindo do sistema. Até logo!")
            break
        else:
            print("Opção inválida. Por favor, escolha uma opção válida.")


def main():
    dados = load_inf()
    menu_principal(dados)


if __name__ == "__main__":
    main()