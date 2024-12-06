import socket
import ssl
import os
import gzip
import hashlib
import logging
from threading import Thread

logging.basicConfig(level=logging.INFO, format="%(asctime)s - %(message)s")

class SecureFileTransferClient:
    def __init__(self, host, port, cafile):
        self.host = host
        self.port = port
        self.context = ssl.create_default_context(cafile=cafile)

    def compress_file(self, file_path, compression_level=9):
        compressed_path = f"{file_path}.gz"
        with open(file_path, 'rb') as f_in:
            with gzip.open(compressed_path, 'wb', compresslevel=compression_level) as f_out:
                f_out.writelines(f_in)
        return compressed_path

    def calculate_checksum(self, file_path):
        sha256_hash = hashlib.sha256()
        with open(file_path, 'rb') as f:
            for byte_block in iter(lambda: f.read(4096), b""):
                sha256_hash.update(byte_block)
        return sha256_hash.hexdigest()

    def send_file(self, file_path, priority=1):
        compressed_path = self.compress_file(file_path)
        file_size = os.path.getsize(compressed_path)
        file_name = os.path.basename(compressed_path)
        checksum = self.calculate_checksum(file_path)

        conn = self.context.wrap_socket(socket.socket(socket.AF_INET), server_hostname=self.host)

        try:
            conn.connect((self.host, self.port))

            # Send metadata
            conn.send(file_name.encode())
            conn.send(str(file_size).encode())
            conn.send(checksum.encode())
            conn.send(str(priority).encode())

            # Get resume position
            resume_position = int(conn.recv(1024).decode())
            logging.info(f"Resuming transfer from byte {resume_position}")

            # Send file
            with open(compressed_path, 'rb') as f:
                f.seek(resume_position)
                sent_size = resume_position
                while chunk := f.read(1024):
                    conn.send(chunk)
                    sent_size += len(chunk)
                    progress = (sent_size / file_size) * 100
                    logging.info(f"Sending {file_name}: {progress:.2f}%")

            logging.info(f"File {file_name} sent successfully!")
        except Exception as e:
            logging.error(f"Error sending file: {e}")
        finally:
            if os.path.exists(compressed_path):
                os.remove(compressed_path)
                logging.info(f"Deleted local compressed file: {compressed_path}")
            conn.close()

    def send_files_in_parallel(self, file_paths):
        threads = []
        for priority, file_path in enumerate(file_paths):
            thread = Thread(target=self.send_file, args=(file_path, host, port, priority))
            threads.append(thread)
            thread.start()

        for thread in threads:
            thread.join()