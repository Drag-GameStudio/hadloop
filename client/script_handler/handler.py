import zipfile
import os
import sys
import tempfile
import importlib.util



class ScriptHandler:
    def __init__(self, script_path):
        self.script_path = script_path

    def client_part(self, data):
        with tempfile.TemporaryDirectory() as temp_dir:
            with zipfile.ZipFile(self.script_path, 'r') as zip_ref:
                zip_ref.extractall(temp_dir)

            project_path = os.path.join(temp_dir, 'script')
            script_path = os.path.join(project_path, 'client_setup.py')

            sys.path.insert(0, project_path)

            spec = importlib.util.spec_from_file_location("client_setup", script_path)
            work_client = importlib.util.module_from_spec(spec)
            spec.loader.exec_module(work_client)
            result = work_client.handle(data)

            return result  
          
    def client_master_part(self, result_list):
        with tempfile.TemporaryDirectory() as temp_dir:
            with zipfile.ZipFile(self.script_path, 'r') as zip_ref:
                zip_ref.extractall(temp_dir)

            project_path = os.path.join(temp_dir, 'script')
            script_path = os.path.join(project_path, 'master_client_setup.py')

            sys.path.insert(0, project_path)

            spec = importlib.util.spec_from_file_location("master_client_setup", script_path)
            work_client = importlib.util.module_from_spec(spec)
            spec.loader.exec_module(work_client)

            result = work_client.compare(result_list)
            return result    
    
# zip_path = r'C:\Users\sinic\OneDrive\Рабочий стол\hadloop\tests_scripts\test1\project.zip'
# sh = ScriptHandler(zip_path)
# result = [sh.client_part("test_data")]
# result = sh.client_master_part(result)
# print(result)  # Output the result from the master client script