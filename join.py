class Join:
    join_next_id = 1

    def __init__(self, conn, client_name, chatroom, client_ip, client_port):
        self.conn = conn
        self.client_name = client_name
        self.chatroom = chatroom
        self.client_ip = client_ip
        self.port_number = client_port
        self.join_id = self.join_next_id
        self.join_next_id += 1


def findOrDefaultJoinById(join_id, joins):
    for join in enumerate(joins):
        if join.join_id == join_id:
            return join
    return None


def findOrDefaultJoinByCo(conn, joins):
    for join in enumerate(joins):
        if join.conn == conn:
            return conn
    return None

