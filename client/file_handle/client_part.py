from settings.hadloop_settings import Settings
import os

class ClientLoader:
    def __init__(self, settings: Settings):
        self.settings = settings

    def save_block(self, block, file_hash):
        name = f"{file_hash}"
        with open(f"{self.settings.root_folder}/{name}", "wb") as file:
            file.write(block)

    def get_block(self, file_hash):
        with open(f"{self.settings.root_folder}/{file_hash}.bin", "rb") as file:
            block = file.read()
        return block
    
    def delete_block(self, file_hash):
        os.remove(f"{self.settings.root_folder}/{file_hash}.bin")

