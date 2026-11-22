import argparse
import csv

from src.assembler import mask

COMMAND_SIZE = 3
REGISTER_COUNT = 32
MEMORY_SIZE = 65536

def decode(cmd):
    """Переводит машинную команду в словарь с полями."""
    A = cmd & mask(4)
    B = (cmd >> 4) & mask(5)

    if A == 1:
        C = (cmd >> 9) & mask(15)
        return {"A": A, "B": B, "C": C}
    if A == 5 or A == 15:
        C = (cmd >> 9) & mask(5)
        return {"A": A, "B": B, "C": C}
    if A == 0:
        C = (cmd >> 9) & mask(9)
        D = (cmd >> 18) & mask(5)
        return {"A": A, "B": B, "C": C, "D": D}

    raise ValueError(f"Неизвестный код команды: {A}")

def execute(bytecode):
    """Выполняет программу и возвращает регистры и память."""
    if len(bytecode) % COMMAND_SIZE != 0:
        raise ValueError("В файле есть неполная команда")
    if len(bytecode) > MEMORY_SIZE:
        raise ValueError("Программа не помещается в память")

    reg = [0] * REGISTER_COUNT
    mem = [0] * MEMORY_SIZE
    mem[:len(bytecode)] = bytecode

    for i in range(0, len(bytecode), COMMAND_SIZE):
        cmd = int.from_bytes(bytes(mem[i:i + 3]), "little")
        fields = decode(cmd)
        A = fields["A"]
        B = fields["B"]
        C = fields["C"]

        if A == 1:
            reg[B] = C
        elif A == 5:
            reg[C] = mem[reg[B]]
        elif A == 0:
            D = fields["D"]
            mem[reg[D] + C] = reg[B]
        elif A == 15:
            raise ValueError("Команда not относится к четвертому этапу")

    return reg, mem

def save_dump(mem, filename, start, end):
    """Сохраняет диапазон памяти в CSV-файл."""
    if start < 0 or end < start or end >= len(mem):
        raise ValueError("Неверный диапазон адресов памяти")

    with open(filename, "w", newline="", encoding="utf-8") as file:
        writer = csv.writer(file)
        writer.writerow(["address", "value"])

        for i in range(start, end + 1):
            writer.writerow([i, mem[i]])

def main():
    parser = argparse.ArgumentParser(description="Интерпретатор УВМ")
    parser.add_argument("--input", required=True)
    parser.add_argument("--output", required=True)
    parser.add_argument("--start", type=int, required=True)
    parser.add_argument("--end", type=int, required=True)
    args = parser.parse_args()

    try:
        with open(args.input, "rb") as file:
            bytecode = file.read()
        reg, mem = execute(bytecode)
        save_dump(mem, args.output, args.start, args.end)
    except (OSError, ValueError) as error:
        parser.error(str(error))

    print("Выполнено команд:", len(bytecode) // COMMAND_SIZE)
    print("Дамп памяти сохранен:", args.output)

if __name__ == "__main__":
    main()