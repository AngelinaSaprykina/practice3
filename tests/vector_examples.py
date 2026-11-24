import json

from src.assembler import asm, asm_bytes
from src.interpreter import execute, save_dump


def create_program(vector):
    """Создает программу обработки вектора."""
    program = [{"op": "load", "b": 0, "c": 200}]

    # Записываем исходный вектор в память
    for i in range(len(vector)):
        program.append({"op": "load", "b": 1, "c": vector[i]})
        program.append({"op": "write", "b": 1, "c": i, "d": 0})

    # Читаем элементы и выполняем побитовое НЕ
    for i in range(len(vector)):
        program.append({"op": "load", "b": 2, "c": 200 + i})
        program.append({"op": "read", "b": 2, "c": 3})
        program.append({"op": "not", "b": 3, "c": 2})

    return program


def practice():
    examples = [
        [0, 1, 2, 3, 4, 5, 6, 7, 8, 9],
        [10, 20, 30, 40, 50, 60, 70, 80, 90, 100],
        [255, 128, 64, 32, 16, 8, 4, 2, 1, 0]
    ]

    for number, vector in enumerate(examples, 1):
        program = create_program(vector)

        with open(f"tests/vector_{number}.json", "w") as file:
            json.dump({"program": program}, file, indent=2)

        bytecode = asm_bytes(asm(program))

        with open(f"vector_{number}.bin", "wb") as file:
            file.write(bytecode)

        reg, mem = execute(bytecode)
        save_dump(mem, f"vector_{number}.csv", 200, 209)

        # Проверяем все 10 результатов
        assert mem[200:210] == [~value for value in vector]

        print(f"Пример {number}: {mem[200:210]}")
        print(f"Команд: {len(program)}, байт: {len(bytecode)}")

    print("Все примеры выполнены успешно")

if __name__ == "__main__":
    practice()