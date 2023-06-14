import socket

def anti_ddos():
    # Configurações do servidor
    HOST = 'localhost'  # Endereço do servidor
    PORT = 8000  # Porta do servidor
    MAX_CONN = 100  # Número máximo de conexões simultâneas

    # Criação do socket
    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)

    # Vincula o socket ao endereço e porta
    server_socket.bind((HOST, PORT))

    # Define o número máximo de conexões pendentes
    server_socket.listen(MAX_CONN)

    print(f"Servidor anti-DDoS iniciado em {HOST}:{PORT}")

    # Loop principal para aceitar conexões e lidar com elas
    while True:
        client_socket, addr = server_socket.accept()
        print(f"Nova conexão recebida de {addr[0]}:{addr[1]}")
        client_socket.send("Conexão estabelecida com sucesso!".encode())
        client_socket.close()

if __name__ == "__main__":
    anti_ddos()
