import argparse
import time
from sys import argv
import socket

# First we use the argparse package to parse the aruments
parser = argparse.ArgumentParser()

parser.add_argument('-f', type=str, default='PROJI-HNS.txt', action='store', dest='in_file')
parser.add_argument('-o', type=str, default='RESOLVED.txt',
                    action='store', dest='out_file')

parser.add_argument('server_location', type=str, help='This is the domain name or ip address of the server',
                    action='store')
parser.add_argument('rsListenPort', type=int, help='This is the port to connect to the server on rsListenPort',
                    action='store')
parser.add_argument('tsListenPort', type=int, help='This is the port to connect to the server on tsListenPort',
                    action='store')
args = parser.parse_args(argv[1:])

rsListenPort = args.rsListenPort
tsListenPort = args.tsListenPort

# next we create a client socket
client_sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
tsclient_sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
tsserver_addr = (args.server_location, tsListenPort)
tsclient_sock.connect(tsserver_addr)
server_addr = (args.server_location, rsListenPort)
client_sock.connect(server_addr)


with open(args.out_file, 'w') as write_file:
    for line in open(args.in_file, 'r'):
# trim the line to avoid weird new line things
        line = line.strip()
# now we write whatever the server tells us to the out_file
        if line:
            client_sock.sendall(line.encode('utf-8'))
            answer = client_sock.recv(256)
# decode answer
            answer = answer.decode('utf-8')
        if "NS" in answer:
            tsclient_sock.sendall(line.encode('utf-8'))
            tsanswer = tsclient_sock.recv(256).decode('utf-8')
            write_file.write(line + tsanswer + '\n')
            continue

        else:
            write_file.write(line + answer + '\n')

# close the socket (note this will be visible to the other side)
tsclient_sock.close()
client_sock.close()
