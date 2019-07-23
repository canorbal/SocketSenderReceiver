import threading
import socket
import logging
import config

receiver_logger = logging.getLogger("ReceiverLogger")


class Receiver:

    def __init__(self):
        # self.host = socket.gethostbyname('localhost')
        self.host = socket.gethostbyname(socket.gethostname())
        self.port = config.PORT

    def receive_info(self):
        receiver_logger.info('Receiving info about filename and threads...')
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as sock:
            sock.bind((self.host, self.port))
            sock.listen()
            (conn, address) = sock.accept()
            self.filename = conn.recv(config.SIZE).decode()
            self.threads_num = int(conn.recv(config.SIZE).decode())

    def receive_data(self):
        receiver_logger.info('Receiving data')
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as sock:
            sock.bind((self.host, self.port))
            sock.listen(self.threads_num)

            threads = []
            self.batches = [None for _ in range(self.threads_num)]

            for thread_index in range(self.threads_num):
                conn, address = sock.accept()

                thread = threading.Thread(
                    target=self._thread_handler, args=(conn, thread_index)
                )
                threads.append(thread)
                thread.start()

            for thread in threads:
                thread.join()

        receiver_logger.info('Data received')

    def _thread_handler(self, conn, thread_index):
        receiver_logger.info(f'Thread {thread_index} receiving data')
        raw_data = None

        index_data = conn.recv(config.SIZE)
        index_data = int(index_data.decode())

        while conn:
            data = conn.recv(config.SIZE)
            if not data:
                break

            if raw_data is None:
                raw_data = data
            else:
                raw_data += data

        self.batches[index_data] = raw_data

    def save_data(self):
        receiver_logger.info('Saving data')

        with open(self.filename, "wb") as f:
            for index in range(self.threads_num):
                f.write(self.batches[index])

        receiver_logger.info('Data saved')
