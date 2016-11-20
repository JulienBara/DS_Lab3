import socket
import sys

from thread import *

from parse import *

import os
import signal

# from multiprocessing import Process
#
# global threads
# threads = []
#
global conns
conns = []

global pids
pids = []

accept_timeout = 10.0
socket_timeout = 60.0


if len(sys.argv) > 3:
    host = str(sys.argv[1])
    port = int(sys.argv[2])
    nbrCoAllowed = int(sys.argv[3])
else:
    host = "localhost"
    port = 3000
    nbrCoAllowed = 10

global s
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


def killsHandler(_sign, _stack_frame):
    global pids
    global conns
    global s

    os.kill(os.getppid(), signal.SIGTERM)

    for conn in conns:
        # conn.close()
        conn.shutdown(socket.SHUT_RDWR)

    for pid in pids:
        os.kill(pid, signal.SIGTERM)

    # os.kill(os.getpid(), signal.SIGTERM)
    s.close()
    s.shutdown(socket.SHUT_RDWR)
    # exit()

signal.signal(signal.SIGTERM, killsHandler)


# Function for handling connections. This will be used to create threads
def clientThread(conn):
    global nbrCoClient
    global serverOn
    # global s
    global pids
    global conns

    conns.append(conn)
    pids.append(os.getpid())

    conn.settimeout(socket_timeout)

    while serverOn:

        try:
            print "Ready to receive"
            data = conn.recv(4096)
        except:
            print "socket timeout"
            break

        if not data:
            break

        print ("received : '" + data + "' from '" + str(conn) + "'")

        if data == "KILL_SERVICE\n":
            serverOn = False
            # s.close()
            # shutdown()
            # killAll()
            print "Shutting down server"
            # interrupt_main()
            os.kill(os.getppid(), signal.SIGTERM)
            break

        elif data[:4] == "HELO":
            text = data[5:]
            conn.send("HELO " + text + "IP:" + host + "\nPort:" + str(port) + "\nStudentID:" + "16337089" + "\n")

        else:
            parse(conn, data, host, port)

    nbrCoClient -= 1

    conns.remove(conn)

    # conn.close()
    conn.shutdown(socket.SHUT_RDWR)
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
            # t = Process(target=clientThread, args=(conn,))
            # threads.append(t)
            # t.start()
            # conns.append(conn)

        except KeyboardInterrupt:
            print "Server stopped from keyboard"
            break

        except socket.timeout:
            print "accept timeout"
            # TODO remove break when debug finished
            # break
            pass
# s.close()
s.shutdown(socket.SHUT_RDWR)
exit()


# def killAll():
#     global threads
#     global conns
#
#     for conn in conns:
#         print ("closing " + str(conn))
#         conn.close()
#
#     for thread in threads:
#         print ("killing " + str(thread))
#         thread.terminate()











