class ClientConn:

    def __init__(self, conn, client_name):
        self.conn = conn
        self.client_name = client_name


def findOrDefaultConnByClientName(client_name, client_conns):
    for client_conn in client_conns:
        if client_conn.client_name == client_name:
            return client_conn
    return None


def findOrCreateClientConnByClientName(conn, client_name, client_conns):
    client_conn = findOrDefaultConnByClientName(client_name, client_conns)
    if client_conn is None:
        client_conn = ClientConn(conn, client_name)
        client_conns.append(client_conn)
    return client_conn
