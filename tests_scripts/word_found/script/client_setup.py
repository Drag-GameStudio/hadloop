from utils import test

def handle(data):
    word = "2019"
    data = data.decode('utf-8') 
    # Найдём все индексы, где начинается подстрока "тест"
    indexes = []
    start = 0
    while True:

        idx = data.find(word, start)
        if idx == -1:
            break
        indexes.append(idx)
        start = idx + 1

    return indexes