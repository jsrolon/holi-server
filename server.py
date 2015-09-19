# Server implementation

from socket import *
import threading

serverPort = 1337

udpSocket = socket(AF_INET, SOCK_DGRAM)
udpSocket.setsockopt(SOL_SOCKET, SO_REUSEADDR, 1)
tcpSocket = socket(AF_INET, SOCK_STREAM)
tcpSocket.setsockopt(SOL_SOCKET, SO_REUSEADDR, 1)

udpSocket.bind(('', serverPort))
print("UDP socket bound")
tcpSocket.bind(('', serverPort))
print("TCP socket bound")

def listenUDP():
    print("UDP socket listening")
    while 1:
        message, clientAddress = udpSocket.recvfrom(2048) 
        modifiedMessage = message.upper() 
        udpSocket.sendto(modifiedMessage, clientAddress)

def listenTCP():
    tcpSocket.listen(0)
    print("TCP socket listening")
    while 1:
        connectionSocket, addr = tcpSocket.accept()
        message = connectionSocket.recv(2048)
        capitalizedSentence = message.upper()
        connectionSocket.send(capitalizedSentence)
        connectionSocket.close()

udpThread = threading.Thread(target=listenUDP, args=())
tcpThread = threading.Thread(target=listenTCP, args=())
udpThread.start()
tcpThread.start()
