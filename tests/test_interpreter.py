import csv
import json
import os

from src.assembler import asm, asm_bytes
from src.interpreter import decode, execute, save_dump

def practice():
    with open("tests/copy_array.json", "r", encoding="utf-8") as file:
        data = json.load(file)

    bytecode = asm_bytes(asm(data["program"]))
    reg, mem = execute(bytecode)

    # Команды и данные лежат в одной памяти
    assert mem[:len(bytecode)] == list(bytecode)
    assert len(bytecode) == 51
    assert reg[4] == 30

    # Проверяем исходный массив и копию
    assert mem[100:103] == [10, 20, 30]
    assert mem[200:203] == [10, 20, 30]

    # Проверяем декодирование команд
    cmd = int.from_bytes(bytecode[:3], "little")
    assert decode(cmd) == {"A": 1, "B": 0, "C": 100}

    cmd = int.from_bytes(bytecode[27:30], "little")
    assert decode(cmd) == {"A": 5, "B": 2, "C": 4}

    cmd = int.from_bytes(bytecode[30:33], "little")
    assert decode(cmd) == {"A": 0, "B": 4, "C": 0, "D": 3}

    # Проверяем содержимое CSV-файла
    save_dump(mem, "test_dump.csv", 200, 202)

    with open("test_dump.csv", "r", encoding="utf-8") as file:
        rows = list(csv.reader(file))

    os.remove("test_dump.csv")

    assert rows == [
        ["address", "value"],
        ["200", "10"],
        ["201", "20"],
        ["202", "30"]
    ]

    print("Все тесты третьего этапа пройдены")

if __name__ == "__main__":
    practice()