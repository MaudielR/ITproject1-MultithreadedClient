#a simplified top-level DNS server

import socket
import sys
import argparse
from sys import argv
import binascii
import struct

CurrentHOST = ''

parser = argparse.ArgumentParser(description="""ts port""")

parser.add_argument('tsListenPort', type=int, action='store')
parser.add_argument('-f', type=str, default='PROJI-DNSTS.txt',action='store', dest='in_file')
args = parser.parse_args(argv[1:])

tsListenPort = args.tsListenPort
table = {}
with open('PROJI-DNSTS.txt', 'r') as file:
    for line in file:
        host, ipAddress, flag = line.strip().split(' ')
        table[host] = ipAddress, flag

# use socket() function to start socket protocal
serverSock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)  # FOR LOCAL CLIENT HANDLING

# bind the server.py to client.py
serverSock.bind((CurrentHOST, tsListenPort))

# after binding, listen to client
serverSock.listen(1)
newSock, serverAddress = serverSock.accept()

# while the server is listening it checks then decodes messages
with newSock:
    while True:
        txtReceived = newSock.recv(512)
        txt = txtReceived.decode('utf-8').lower()
        if not txtReceived:
            break
        if txt in table:
            text = table.get(txt)
            print(text)
            untuplemessage = " "+ text[0] +" " + text[1]
            newSock.send(untuplemessage.encode('utf-8'))
            #newSock.close()
        else:
            # If there is no match, RS sends the string
            text = "  - Error:HOST NOT FOUND"
            newSock.send(text.encode('utf-8'))
        socket.setdefaulttimeout(10)
# close socket
newSock.close()
