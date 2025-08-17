import httpx
import asyncio
from menu.models import LocalFilePosition, File, Client
from script_handler.handler import ScriptHandler

async def run_script_fetch_block(client, file, script_file):
    files = {
            "script_file": (str(script_file), script_file, "application/zip")
    }
    print(f"Run script on {file[1]} for file {file[0]}")
    response = await client.post(
        f"{file[1]}/file_handler/run_script",
        data={"file_name": file[0]},
        files=files
    )
    response.raise_for_status()
    return response.json()["result"]

async def run_script_async(all_files_position, script_file):
    async with httpx.AsyncClient(timeout=None) as client:
        tasks = [run_script_fetch_block(client, file, script_file) for file in all_files_position]
        blocks = await asyncio.gather(*tasks)

    # Собираем файл из всех блоков
    return blocks


def run_script_on_file(file_name, script_file):
    global_file = File.objects.filter(file_name=file_name).first()
    if global_file is None:
        return -1
    all_files_position: list[LocalFilePosition] = list(global_file.local_file_position.all())
    all_files_position.sort()

    all_data = [[el.file_hash, el.client_position.ip] for el in all_files_position]
    
    with open("script_handler/all_scripts/" + str(script_file), "wb") as f:
        f.write(script_file.read())

    results = asyncio.run(run_script_async(all_data, script_file))

    sh = ScriptHandler("script_handler/all_scripts/" + str(script_file))
    result = sh.client_master_part(results)
    return result