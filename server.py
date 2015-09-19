# #
# HOLI Server canonical implementation
# v0.1
# #

# imports
from socket import *
import threading
import datetime
import logging
import sys

serverPort = 1337

# Start
print("\nHOLI Server Canonical Implementation\nVersion 0.1\nSeptember 2015\n-------\n")
logging.basicConfig(stream=sys.stdout, level=logging.DEBUG)

# Socket creation and options
udpSocket = socket(AF_INET, SOCK_DGRAM)
udpSocket.setsockopt(SOL_SOCKET, SO_REUSEADDR, 1)
tcpSocket = socket(AF_INET, SOCK_STREAM)
tcpSocket.setsockopt(SOL_SOCKET, SO_REUSEADDR, 1)

# Binding sockets
udpSocket.bind(('', serverPort))
logging.info("UDP Socket Bound")
tcpSocket.bind(('', serverPort))
logging.info("TCP Socket Bound")

# Output file
of = open("reports/" + str(datetime.datetime.now().strftime('%Y%m%d_%H%M%S')) + ".csv", "w")

def closeServer():
    print("\nServer closing...")
    of.close()
    udpSocket.close()
    tcpSocket.close()
    print("Done")

# Functions
def listenUDP():
    logging.info("UDP socket listening")
    while 1:
        message, clientAddress = udpSocket.recvfrom(2048)
        msg = message.decode("utf-8")
        print(str(datetime.datetime.now()) + " :: " + clientAddress[0] + " :: UDP :: " + msg.replace(";", "\t"))
        print("UDP;" + clientAddress[0] + ";" + msg, file=of)


def listenTCP():
    tcpSocket.listen(0)
    logging.info("TCP socket listening")
    while 1:
        connectionSocket, clientAddress = tcpSocket.accept()
        message = connectionSocket.recv(2048)
        connectionSocket.close()
        msg = message.decode("utf-8")
        print(str(datetime.datetime.now()) + " :: " + clientAddress[0]  + " :: TCP :: " + msg.replace(";", "\t"))
        print("TCP;" + clientAddress[0] + ";"  + msg, file=of)

try:
    # create daemon threads so that the keyboard interrupt is handled
    udpThread = threading.Thread(target=listenUDP, args=())
    udpThread.daemon = True

    tcpThread = threading.Thread(target=listenTCP, args=())
    tcpThread.daemon = True

    udpThread.start()
    tcpThread.start()

    # wait for the threads to finish (that's never)
    udpThread.join()
except KeyboardInterrupt:
    closeServer()
