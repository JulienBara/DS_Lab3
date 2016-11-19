from helper import *


# TODO We could check integrity of each line in if
def parse(conn, data, host, port):

    lines = data.split("\n")

    if lines[0][:15] == "JOIN_CHATROOM: ":
        chatroom_name = lines[0][15:]
        client_ip = lines[1][11:]
        client_port = lines[2][6:]
        client_name = lines[3][13:]
        joining(conn, chatroom_name, client_ip, client_port, client_name, host, port)

    if lines[0][:16] == "LEAVE_CHATROOM: ":
        chatroom_id = lines[0][16:]
        join_id = lines[1][9:]
        client_name = lines[2][13:]
        leaving(conn, chatroom_id, join_id, client_name)

    if lines[0][:12] == "DISCONNECT: ":
        client_ip = lines[0][12:]
        client_port = lines[1][6:]
        client_name = lines[2][13:]
        disconnect(conn, client_ip, client_port, client_name)

    if lines[0][:6] == "CHAT: ":
        chatroom_id = lines[0][6:]
        join_id = lines[1][9:]
        client_name = lines[2][13:]
        message = lines[3][9:]
        messaging(conn, chatroom_id, join_id, client_name, message)
