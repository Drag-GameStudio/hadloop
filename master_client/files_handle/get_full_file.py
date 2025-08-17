import httpx
import asyncio
from menu.models import LocalFilePosition, File, Client
from script_handler.handler import ScriptHandler
import base64

async def get_full_file_fetch_block(client, file):
    response = await client.get(
        f"{file[1]}/file_handler/",
        params={"file_name": file[0]}
    )
    response.raise_for_status()
    return base64.b64decode(response.json()["block"])

async def get_full_file_async(all_files_position):
    async with httpx.AsyncClient(timeout=None) as client:
        tasks = [get_full_file_fetch_block(client, file) for file in all_files_position]
        blocks = await asyncio.gather(*tasks)

    # Собираем файл из всех блоков
    full_file = b''.join(blocks)
    return full_file

def get_full_file(file_name):
    global_file = File.objects.filter(file_name=file_name).first()
    if global_file is None:
        return -1
    all_files_position: list[LocalFilePosition] = list(global_file.local_file_position.all())
    all_files_position.sort()

    all_data = [[el.file_hash, el.client_position.ip] for el in all_files_position]


    result = asyncio.run(get_full_file_async(all_data))
    return result