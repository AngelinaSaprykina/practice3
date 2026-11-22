import argparse
import json

from src.assembler import asm, asm_bytes

def main():
    parser = argparse.ArgumentParser(
        description="Ассемблер УВМ, вариант 28"
    )

    parser.add_argument("--input", required=True)
    parser.add_argument("--output", required=True)
    parser.add_argument("--test", action="store_true")

    args = parser.parse_args()

    try:
        with open(args.input, "r", encoding="utf-8") as file:
            data = json.load(file)

        program = data["program"]
        result = asm(program)
        machine_code = asm_bytes(result)

        with open(args.output, "wb") as file:
            file.write(machine_code)

    except (OSError, ValueError, KeyError, TypeError) as error:
        parser.error(str(error))

    if args.test:
        for cmd in result:
            print(", ".join(
                f"{key}={value}" for key, value in cmd.items()
            ))

        print("Машинный код:")

        for i in range(0, len(machine_code), 3):
            command = machine_code[i:i + 3]
            print(", ".join(f"0x{b:02X}" for b in command))

    print("Команд обработано:", len(result))
    print("Размер файла:", len(machine_code), "байт")
    print("Файл сохранен:", args.output)

if __name__ == "__main__":
    main()