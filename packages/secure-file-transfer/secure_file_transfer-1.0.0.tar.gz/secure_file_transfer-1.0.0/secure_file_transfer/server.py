import socket
import ssl
import os
import gzip
import hashlib
import logging
import threading
from queue import PriorityQueue

logging.basicConfig(level=logging.INFO, format="%(asctime)s - %(message)s")

class SecureFileTransferServer:
    def __init__(self, host, port, certfile, keyfile):
        self.host = host
        self.port = port
        self.context = ssl.create_default_context(ssl.Purpose.CLIENT_AUTH)
        self.context.load_cert_chain(certfile=certfile, keyfile=keyfile)
        self.transfer_queue = PriorityQueue()

    def calculate_checksum(self, file_path):
        sha256_hash = hashlib.sha256()
        with open(file_path, 'rb') as f:
            for byte_block in iter(lambda: f.read(4096), b""):
                sha256_hash.update(byte_block)
        return sha256_hash.hexdigest()

    def decompress_file(self, file_path):
        decompressed_path = file_path.replace(".gz", "")
        with gzip.open(file_path, 'rb') as f_in:
            with open(decompressed_path, 'wb') as f_out:
                f_out.write(f_in.read())

        if os.path.exists(file_path):
            os.remove(file_path)
            logging.info(f"Deleted server compressed file: {file_path}")
        return decompressed_path

    def handle_client(self, conn, addr):
        try:
            file_name = conn.recv(1024).decode()
            file_size = int(conn.recv(1024).decode())
            file_checksum = conn.recv(1024).decode()
            priority = int(conn.recv(1024).decode())

            self.transfer_queue.put((priority, conn, addr, file_name, file_size, file_checksum))
        except Exception as e:
            logging.error(f"Error handling client {addr}: {e}")

    def process_transfers(self):
        while True:
            if not self.transfer_queue.empty():
                priority, conn, addr, file_name, file_size, file_checksum = self.transfer_queue.get()

                try:
                    received_size = 0
                    if os.path.exists(f"received_{file_name}.gz"):
                        received_size = os.path.getsize(f"received_{file_name}.gz")
                        conn.send(str(received_size).encode())
                    else:
                        conn.send(b"0")

                    with open(f"received_{file_name}.gz", 'ab') as f:
                        while received_size < file_size:
                            chunk = conn.recv(1024)
                            if not chunk:
                                break
                            f.write(chunk)
                            received_size += len(chunk)
                            progress = (received_size / file_size) * 100
                            logging.info(f"Receiving {file_name} (Priority {priority}): {progress:.2f}%")

                    decompressed_path = self.decompress_file(f"received_{file_name}.gz")
                    received_checksum = self.calculate_checksum(decompressed_path)

                    if received_checksum == file_checksum:
                        logging.info(f"File {file_name} received successfully!")
                    else:
                        logging.warning(f"Checksum mismatch for {file_name}, retrying transfer...")
                        self.transfer_queue.put((priority, conn, addr, file_name, file_size, file_checksum))
                except Exception as e:
                    logging.error(f"Error processing transfer: {e}")
                finally:
                    conn.close()

    def start(self):
        server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        server_socket.bind((self.host, self.port))
        server_socket.listen(5)
        logging.info(f"Server listening on {self.host}:{self.port}")

        threading.Thread(target=self.process_transfers, daemon=True).start()

        while True:
            conn, addr = server_socket.accept()
            conn = self.context.wrap_socket(conn, server_side=True)
            threading.Thread(target=self.handle_client, args=(conn, addr)).start()
