import socket
import sys

from thread import *

from parse import *


accept_timeout = 20.0
socket_timeout = 0.0001


if len(sys.argv) > 3:
    host = str(sys.argv[1])
    port = int(sys.argv[2])
    nbrCoAllowed = int(sys.argv[3])
else:
    host = "localhost"
    port = 3000
    nbrCoAllowed = 10

s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
print "socket created"

# Bind socket to local host and port
try:
    s.bind((host, port))
except socket.error as msg:
    print ('Bind failed. Error Code : ' + str(msg[0]) + ' Message ' + msg[1])
    sys.exit()

print 'Socket bind complete'

# Start listening on socket
s.listen(10)
print 'Socket now listening'

global serverOn
serverOn = True

global nbrCoClient
nbrCoClient = 0

# Function for handling connections. This will be used to create threads
def clientThread(conn):
    conn.settimeout(socket_timeout)

    global nbrCoClient
    global serverOn
    while serverOn:

        try:
            print "Ready to receive"
            data = conn.recv(4096)
        except:
            print "socket timeout"
            continue
            break

        if not data:
            break

        print ("received : '" + data + "' from '" + str(conn) + "'")

        if data == "KILL_SERVICE\n":
            serverOn = False
            print "Shutting down server"

        elif data[:4] == "HELO":
            text = data[5:]
            conn.send("HELO " + text + "IP:" + host + "\nPort:" + str(port) + "\nStudentID:" + "16337089" + "\n")

        else:
            parse(conn, data, host, port)

    nbrCoClient -= 1
    conn.close()
    exit()


while serverOn:
    if nbrCoAllowed > nbrCoClient:
        # wait to accept a connection - blocking call
        s.settimeout(accept_timeout)
        try:
            conn, addr = s.accept()
            nbrCoClient += 1

            print ('Connected with ' + addr[0] + ':' + str(addr[1]))

            if not serverOn:
                break

            # start new thread takes 1st argument as a function name to be run, second is the tuple of arguments to the function.
            start_new_thread(clientThread, (conn,))
        except:
            print "accept timeout"
            # TODO remove break when debug finished
            break
            continue
s.close()
exit()










