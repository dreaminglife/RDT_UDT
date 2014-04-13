from socket import socket, AF_INET, SOCK_DGRAM
from sys import argv
from common import ip_checksum


if __name__ == "__main__":
    dest_addr = argv[1]
    dest_port = int(argv[2])
    dest = (dest_addr, dest_port)
    listen_addr = argv[3]
    listen_port = int(argv[4])
    listen = (listen_addr, listen_port)

    send_sock = socket(AF_INET, SOCK_DGRAM)
    recv_sock = socket(AF_INET, SOCK_DGRAM)

    recv_sock.bind(listen)

    while True:
        message, address = recv_sock.recvfrom(4096)

        checksum = message[:2]
        content = message[2:]

        if ip_checksum(content) == checksum:
            send_sock.sendto("ACK", dest)
            print content,
        else:
            send_sock.sendto("NAK", dest)
