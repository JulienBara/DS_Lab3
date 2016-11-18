import socket
import sys

if len(sys.argv) > 2:
    host = str(sys.argv[1])
    port = int(sys.argv[2])
else:
    host = "10.62.0.229"
    port = 3000

socketClient = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
socketClient.settimeout(60.0)

try :
    socketClient.connect((host, port))
except :
    print 'Connection error'
    sys.exit()

while 1:
    # print socketClient.recv(4096)
    
    msg = raw_input("What is your message? (X to quit): ")

    if msg == 'X' or msg == 'x':
        socketClient.close()
        break

    else:
        socketClient.send(msg + "\n")
        try:
            data = socketClient.recv(4096)
        except:
            socketClient.close()
            print ("disconnected")
            break
        print data
