global join_next_id
join_next_id = 1


class Join:

    def __init__(self, conn, client_name, chatroom, client_ip, client_port):
        global join_next_id
        self.conn = conn
        self.client_name = client_name
        self.chatroom = chatroom
        self.client_ip = client_ip
        self.client_port = client_port
        self.join_id = join_next_id
        join_next_id += 1


def findOrDefaultJoinById(join_id, joins):
    for join in joins:
        if join.join_id == join_id:
            return join
    return None


def findOrDefaultJoinByCo(conn, joins):
    for join in joins:
        if join.conn == conn:
            return join
    return None


def findOrDefaultJoinByChatroom(chatroom, joins):
    for join in joins:
        if join.chatroom == chatroom:
            return join
    return None

