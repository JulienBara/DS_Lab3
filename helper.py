import time

from chatroom import *
from join import *

global chatrooms
chatrooms = []

global joins
joins = []


def joining(conn, chatroom_name, client_ip, client_port, client_name, host, port):
    global chatrooms
    global joins

    chatroom = findOrCreateChatroomByName(chatroom_name, chatrooms)
    join = Join(conn, client_name, chatroom, client_ip, client_port)

    joins.append(join)
    chatroom.joins.append(join)

    s = "JOINED_CHATROOM:" + join.chatroom.chatroom_name + "\n" \
        + "SERVER_IP:" + host + "\n"                            \
        + "PORT:" + str(port) + "\n"                            \
        + "ROOM_REF:" + str(join.chatroom.chatroom_id) + "\n"   \
        + "JOIN_ID:" + str(join.join_id) + "\n"
    sendingMessageToCo(conn, s)
    s = "CHAT:" + str(join.chatroom.chatroom_id) + "\n"   \
        + "CLIENT_NAME:" + client_name + "\n"        \
        + "MESSAGE:" + client_name + " has joined this chatroom.\n\n"
    sendingMessageToAllClientsOfChatroom(chatroom, s)


# TODO Opti en requetant d'abord le join puis en testant si bonne chatroom
def leaving(conn, chatroom_id, join_id, client_name):
    global chatrooms
    global joins

    s = "LEFT_CHATROOM:" + chatroom_id + "\n" \
        + "JOIN_ID:" + join_id + "\n"
    sendingMessageToCo(conn, s)

    #TODO for the moment we are assuming chatroom_id and join_id are coherent by user, we may have to check that
    chatroom = findOrDefaultChatroomById(int(chatroom_id), chatrooms)
    if chatroom is not None:
        join = findOrDefaultJoinById(join_id, joins)
        if join is not None:
            s = "CHAT:" + chatroom_id + "\n" \
                + "CLIENT_NAME:" + client_name + "\n" \
                + "MESSAGE:" + client_name + " has left this chatroom.\n\n"
            sendingMessageToAllClientsOfChatroom(join.chatroom, s)

            join.chatroom.removeExistingJoinInChatroom(join)
            joins.remove(join)


# TODO Opti en requetant d'abord le join puis en testant si bonne chatroom
def messaging(conn, chatroom_id, join_id, client_name, message):
    global chatrooms
    global joins

    chatroom = findOrDefaultChatroomById(int(chatroom_id), chatrooms)
    if chatroom is not None:
        join = findOrDefaultJoinById(int(join_id))
        if join is not None:
            if chatroom.findOrDefaultJoinInChatroom(join) is not None:
                s = "CHAT:" + str(join.chatroom.chatroom_id) + "\n" \
                    + "CLIENT_NAME:" + join.client_name + "\n"      \
                    + "MESSAGE:" + message + "\n\n"
                sendingMessageToAllClientsOfChatroom(join.chatroom, s)


def disconnect(conn, client_ip, client_port, client_name):
    global chatrooms

    for chatroom in chatrooms:
        join = findOrDefaultJoinByCo(conn, chatroom.join)
        if join is not None:
            leaving(conn, join.chatroom.chatroom_id, join.join_id, join.client_name)
    conn.close()


def error(conn, number):
    s = "ERROR_CODE:"

    if number == 1:
        s += "1\n" \
            + "ERROR_DESCRIPTION:No matching command.\n\n"

    sendingMessageToCo(conn, s)


def sendingMessageToCo(conn, message):
    conn.send(message)
    print ("sent : '" + message + "' to '" + str(conn) + "'")


def sendingMessageToAllClientsOfChatroom(chatroom, message):
    for join in chatroom.joins:
        sendingMessageToCo(join.conn, message)


