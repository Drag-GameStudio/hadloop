import threading
from abc import ABC, abstractmethod
import os
import hashlib
import requests
from settings.hadloop_settings import Settings
from menu.models import Client, LocalFilePosition, File
import base64
import httpx
import asyncio
from .run_scripts import run_script_on_file
from .get_full_file import get_full_file



def get_random_hash(random_param=32):
    random_bytes = os.urandom(random_param)
    hash_value = hashlib.sha256(random_bytes).hexdigest()

    return hash_value


class Loader(ABC):
    def __init__(self, file_name, file):
        self.file = file
        self.gloval_file_db = File.objects.create(file_name=file_name)
        

    def send_block(self, block, file_hash, client_link):
        files = {
            "file": (f"{file_hash}.bin", block)
        }
        requests.post(f"{client_link}/file_handler/upload",files=files)
        print(f"send file to {client_link} {file_hash}")

    def reader(self, chunk_size):
        buffer = b''
        while chunk := self.file.read(chunk_size):
            is_last = len(chunk) < chunk_size
            chunk = buffer + chunk

            if is_last == False:

                last_index = chunk.rfind(b"\n")
                if last_index == -1:
                    buffer = b''
                else:
                    buffer = chunk[last_index + 1:]
                    chunk = chunk[:last_index + 1]
                
                
                yield chunk
            else:
                yield chunk

    def split_info(self, block_size, max_client_size):
        response_data = []

        all_clients = Client.objects.all()
        links = [el.ip for el in all_clients]

        for i, el in enumerate(self.reader(block_size)):
            
            client_index = (i // max_client_size) % len(links)
            current_client_link = links[client_index]

            file_hash = get_random_hash()

            lfp = LocalFilePosition.objects.create(file_hash=file_hash, file_id=i, global_file=self.gloval_file_db, client_position=all_clients[client_index])

            send = threading.Thread(target=self.send_block, args=(el, file_hash, current_client_link))       
            send.start()
            response_data.append([i, file_hash])

        return response_data
           


def send_file_to_client(file, file_name, settings: Settings):
    httpl = Loader(file=file, file_name=file_name)
    httpl.split_info(settings.block_size, settings.client_max_size)
    httpl.gloval_file_db.is_ready = True
    httpl.gloval_file_db.save()

def delete_file(file_name):
    global_file = File.objects.filter(file_name=file_name).first()
    if global_file is None:
        return -1
    all_files_position: list[LocalFilePosition] = global_file.local_file_position.all()
    for file in all_files_position:
        requests.post(f"{file.client_position.ip}/file_handler/delete", data={"file_name": file.file_hash})

    global_file.delete()





