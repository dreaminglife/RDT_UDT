# interceptor.py
# Man in the Middle unreliable channel simulator.
# Delays, corrupts, and drops UDP packets on the specified ports.
# For CMPT 371
# Author: James Twigg
# March 25 2014

from socket import *
import random
import time


def usage():
    print("Usage: python interceptor.py FromSenderPort ToReceiverPort FromReceiverPort ToSenderPort")
    exit()


def randSleep():

    # 延迟时间：80ms~120ms
    delay = random.random() * 0.02
    sign = random.randint(0, 1)
    if (sign == 1):
        delay = -delay
    delay += 0.1
    time.sleep(delay)


def corrupt(pkt):
    # 损坏函数：
    index = random.randint(0, len(pkt)-1)
    pkt = pkt[:index] + str(chr(random.randint(0, 95))) + pkt[index+1:]
    return pkt


def intercept(pkt, outSock, addr):

    # 0.5正常发送，0.25丢包，0.25损坏
    rand = random.randint(1, 20)
    if rand >= 1 and rand <= 5:
        print("Dropped")
        return
    if rand >= 6 and rand <= 10:
        pkt = corrupt(pkt)
        print("Corrupted to:", pkt)
    #
    randSleep()
    outSock.sendto(pkt, addr)

from sys import argv
if len(argv) < 5:
    usage()

# 定义ip地址和端口号
fromSenderAddr = ('localhost', int(argv[1]))
toReceiverAddr = ('localhost', int(argv[2]))
fromReceiverAddr = ('localhost', int(argv[3]))
toSenderAddr = ('localhost', int(argv[4]))

# 套接字
fromSenderSock = socket(AF_INET, SOCK_DGRAM)
fromSenderSock.bind(fromSenderAddr)
fromSenderSock.setblocking(0)
fromReceiverSock = socket(AF_INET, SOCK_DGRAM)
fromReceiverSock.bind(fromReceiverAddr)
fromReceiverSock.setblocking(0)

outSock = socket(AF_INET, SOCK_DGRAM)
print("Listening...")
while True:
    try:
        pkt = fromSenderSock.recv(4096)
        print("Received packet from sender:", pkt)
        intercept(pkt, outSock, toReceiverAddr)
    except error:
        pass
    try:
        pkt = fromReceiverSock.recv(4096)
        print("Received packet from receiver:", pkt)
        intercept(pkt, outSock, toSenderAddr)
    except error:
        pass
