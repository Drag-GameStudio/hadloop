from utils import test

def compare(result_list):
    all_len = 0
    # [all_len + len(result) for result in result_list]
    for result in result_list:
        all_len += result
    return all_len