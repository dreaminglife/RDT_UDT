from socket import socket, AF_INET, SOCK_DGRAM, timeout
from sys import argv
from common import ip_checksum


SEGMENT_SIZE = 100

if __name__ == "__main__":

    # 发送端口和接收端口
    dest_port = int(argv[1])
    dest = ("127.0.0.1", dest_port)

    listen_port = int(argv[2])
    listen = ("127.0.0.1", listen_port)
    filename = argv[3]

    with open(filename) as f:
        content = f.read()

    # 建立套接字
    send_sock = socket(AF_INET, SOCK_DGRAM)
    recv_sock = socket(AF_INET, SOCK_DGRAM)


    recv_sock.bind(listen)
    recv_sock.settimeout(1)

    offset = 0
    seq = 0


    while offset < len(content):
        if offset + SEGMENT_SIZE > len(content):
            segment = content[offset:]
        else:
            segment = content[offset:offset + SEGMENT_SIZE]
        offset += SEGMENT_SIZE

        ack_received = False
        while not ack_received:
            # 校验和+序列(0,1)+数据
            send_sock.sendto(ip_checksum(segment) + str(seq) + segment, dest)

            try:
                message, address = recv_sock.recvfrom(4096)
            except timeout:
                print("Timeout")
            else:
                print(message)
                checksum = message[:2]
                ack_seq = message[5]
                # 检验 排序
                if ip_checksum(message[2:]) == checksum and ack_seq == str(seq):
                    ack_received = True

        seq = 1 - seq
