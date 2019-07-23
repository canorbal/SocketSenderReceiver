import time
import threading
import socket
import pathlib
import logging
import config

sender_logger = logging.getLogger("SenderLogger")


class Sender:

    def __init__(self, ip, file, threads):
        # self.host = 'localhost'
        self.host = ip
        self.path = pathlib.Path(file)
        self.filename = self.path.parts[-1]
        self.threads_num = threads
        self.port = config.PORT

    def send_info(self):
        sender_logger.info('Sending information about filename and threads number...')
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as sock:
            sock.connect((self.host, self.port))
            sock.send(self.filename.encode())
            time.sleep(config.TIME_SLEEP)
            sock.send(str(self.threads_num).encode())

    def send_data(self):
        if not self.path.exists():
            raise FileNotFoundError()
        
        sender_logger.info('Sending data...')
        threads = [None for _ in range(self.threads_num)]

        batch_size = self.path.stat().st_size // self.threads_num + 1

        for thread_index in range(self.threads_num):
            start_position = thread_index * batch_size
            thread = threading.Thread(
                target=self._thread_handler,
                args=(self.path, thread_index, batch_size, start_position)
            )

            threads[thread_index] = thread
            thread.start()

        for thread in threads:
            thread.join()

        sender_logger.info('Data sent')

    def _thread_handler(self, path, thread_index, batch_size, start_from):
        sender_logger.info(f'Thread {thread_index} is sending')
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as sock:
            sock.connect((self.host, self.port))
            sock.send(str(thread_index).encode())
            time.sleep(config.TIME_SLEEP)

            with open(path, 'rb') as f:
                f.seek(start_from)
                raw_data = f.read(batch_size)
                sock.send(raw_data)
