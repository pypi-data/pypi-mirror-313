import socket

from phound.logging import logger


class Connection:
    def __init__(self, conn: socket.socket) -> None:
        self.file = conn.makefile('r')
        self._conn = conn

    def close(self) -> None:
        logger.info("Closing connection")
        self.file.close()
        self._conn.close()


class Server:
    def __init__(self) -> None:
        self.sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        self.sock.bind(("127.0.0.1", 0))
        self.sock.listen(5)

    def get_new_connection(self) -> Connection:
        conn, _ = self.sock.accept()
        return Connection(conn)

    @property
    def port(self) -> int:
        return self.sock.getsockname()[1]
