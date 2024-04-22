import socket
import struct
import threading

# Configuração inicial
HOST = '0.0.0.0'
PORT = 80
THRESHOLD = 1000  # Número de pacotes por segundo para considerar um ataque DDoS

# Contador de pacotes
packet_counts = {}

# Bloqueio para sincronizar o acesso ao contador de pacotes
lock = threading.Lock()

def monitor_traffic():
    global packet_counts
    with socket.socket(socket.AF_PACKET, socket.SOCK_RAW, socket.ntohs(0x0003)) as s:
        while True:
            packet, _ = s.recvfrom(65565)
            # Desempacota o pacote para obter o endereço IP de origem
            ip_header = packet[14:34]
            iph = struct.unpack('!BBHHHBBH4s4s', ip_header)
            src_ip = socket.inet_ntoa(iph[8])
            
            # Atualiza o contador de pacotes
            with lock:
                if src_ip in packet_counts:
                    packet_counts[src_ip] += 1
                else:
                    packet_counts[src_ip] = 1

def detect_ddos():
    global packet_counts
    while True:
        with lock:
            for src_ip, count in packet_counts.items():
                if count > THRESHOLD:
                    print(f"Detectado possível ataque DDoS de {src_ip}")
            packet_counts = {}  # Reseta o contador
        time.sleep(1)

# Inicia as threads de monitoramento e detecção
traffic_thread = threading.Thread(target=monitor_traffic)
ddos_thread = threading.Thread(target=detect_ddos)

traffic_thread.start()
ddos_thread.start()
