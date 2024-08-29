import socket
import os


def criar_arquivo_exemplo(caminho):
    conteudo_exemplo = """192.168.0.1:80,443
192.168.0.2:22,8080
192.168.0.3:21,23"""
    with open(caminho, 'w') as arquivo:
        arquivo.write(conteudo_exemplo)


def main():
    # Obtém o caminho do diretório atual do script
    meu_caminho = os.path.dirname(os.path.abspath(__file__))
    print(f"Executando de: {meu_caminho}")

    # Caminho para o arquivo .dat com IPs e portas para testar
    caminho_arquivo_dados = os.path.join(meu_caminho, 'data.dat')

    # Imprime o caminho do arquivo para verificar se está correto
    print(f"Caminho do arquivo de dados: {caminho_arquivo_dados}")

    # Verifica se o arquivo existe, se não existir, cria um arquivo de exemplo
    if not os.path.exists(caminho_arquivo_dados):
        print(f"Arquivo {caminho_arquivo_dados} não encontrado. Criando arquivo de exemplo.")
        criar_arquivo_exemplo(caminho_arquivo_dados)

    # Lê o conteúdo do arquivo .dat na memória
    try:
        with open(caminho_arquivo_dados, 'r') as arquivo:
            conteudo_bruto_arquivo = arquivo.readlines()
    except FileNotFoundError:
        print(f"Arquivo não encontrado: {caminho_arquivo_dados}")
        return

    # Listas para conexões bem-sucedidas e mal-sucedidas
    conexoes_sucesso = []
    conexoes_falha = []

    # Processa as linhas e tenta as conexões
    for linha in conteudo_bruto_arquivo[:10]:  # Limita a 10 linhas
        destino, portas = linha.strip().split(":")
        portas = portas.split(",")

        for porta_destino in portas:
            tcp = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            tcp.settimeout(1)  # Define timeout de 1 segundo
            try:
                tcp.connect((destino, int(porta_destino)))
                print(f"\033[91mConexão bem-sucedida para {destino}:{porta_destino}\033[0m")
                conexoes_sucesso.append(f"{destino}:{porta_destino}")
                tcp.close()
            except Exception:
                print(f"\033[92mConexão bloqueada com sucesso {destino}:{porta_destino}\033[0m")
                conexoes_falha.append(f"{destino}:{porta_destino}")

    # Verifica se todas as conexões foram bloqueadas
    aprovado = len(conexoes_sucesso) == 0
    mensagem_aprovado = "Parabéns! Você bloqueou todas as tentativas de exfiltração de dados."
    mensagem_reprovado = "Desculpe, você precisa investigar por que nem todas as conexões foram bloqueadas. Tente novamente!"

    print("\033[93m--------------------------------------")
    print("Resumo")
    print("--------------------------------------")
    print("STATUS: ", end='')
    if aprovado:
        print("\033[92mAprovado!\033[0m")
        print(f"\033[92m{mensagem_aprovado}\033[0m")
    else:
        print("\033[91mReprovado!\033[0m")
        print(f"\033[91m{mensagem_reprovado}\033[0m")

    print(f"Conexões bloqueadas: {len(conexoes_falha)}")
    print(f"Conexões bem-sucedidas: {len(conexoes_sucesso)}")

    # Mostra as conexões bem-sucedidas para verificação
    if len(conexoes_sucesso) > 0:
        print("---- LISTA DE CONEXÕES PARA VERIFICAÇÃO -----")
        for conexao in conexoes_sucesso:
            print(conexao)


if __name__ == "__main__":
    main()
