from helper import *


def parse(conn, data, host, port):

    print "Now in parse"

    lines = data.split("\n")

    if lines[0][:14] == "JOIN_CHATROOM:":

        print "Now in case join_chatroom"

        chatroom_name = lines[0][14:]
        client_ip = lines[1][10:]
        client_port = lines[2][5:]
        client_name = lines[3][12:]
        joining(conn, chatroom_name, client_ip, client_port, client_name, host, port)

    elif lines[0][:15] == "LEAVE_CHATROOM:":

        print "Now in case leave_chatroom"

        chatroom_id = lines[0][15:]
        join_id = lines[1][8:]
        client_name = lines[2][12:]
        leaving(conn, chatroom_id, join_id, client_name)

    elif lines[0][:11] == "DISCONNECT:":

        print "Now in case disconnect"

        client_ip = lines[0][11:]
        client_port = lines[1][5:]
        client_name = lines[2][12:]
        disconnect(conn, client_ip, client_port, client_name)

    elif lines[0][:5] == "CHAT:":

        print "Now in case chat"

        chatroom_id = lines[0][5:]
        join_id = lines[1][8:]
        client_name = lines[2][12:]
        message = lines[3][8:]
        messaging(conn, chatroom_id, join_id, client_name, message)

    else:

        print "Now in case no match"

        error(conn, 1)
