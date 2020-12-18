from socket import socket, AF_INET, SOCK_DGRAM
from sys import argv, stdout
from common import ip_checksum


def send(content, to):
    checksum = ip_checksum(content)
    send_sock.sendto(checksum + content, to)

if __name__ == "__main__":
    dest_port = int(argv[1])
    dest = ("127.0.0.1", dest_port)
    listen_port = int(argv[2])
    listen = ("127.0.0.1", listen_port)

    send_sock = socket(AF_INET, SOCK_DGRAM)
    recv_sock = socket(AF_INET, SOCK_DGRAM)

    recv_sock.bind(listen)

    expecting_seq = 0

    while True:
        message, address = recv_sock.recvfrom(4096)

        checksum = message[:2]
        seq = message[2]
        content = message[3:]

        if ip_checksum(content) == checksum:
            send("ACK" + seq, dest)
            if seq == str(expecting_seq):
                stdout.write(content)
                expecting_seq = 1 - expecting_seq
        else:
            negative_seq = str(1 - expecting_seq)
            send("ACK" + negative_seq, dest)
