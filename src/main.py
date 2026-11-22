import argparse
import json

from src.assembler import asm

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

    except (OSError, ValueError, KeyError, TypeError) as error:
        parser.error(str(error))

    if args.test:
        for cmd in result:
            print(", ".join(
                f"{key}={value}" for key, value in cmd.items()
            ))

    print("Команд обработано:", len(result))

if __name__ == "__main__":
    main()