from utils import test

def compare(result_list):
    exit_data = []
    for result in result_list:
        [exit_data.append(el) for el in result]
    return exit_data