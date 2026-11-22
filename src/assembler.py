def mask(n):
    return 2 ** n - 1

def check_value(value, bits):
    """Проверяет значение поля команды."""
    if type(value) is not int:
        raise ValueError("Значение должно быть целым числом")

    if value < 0 or value > mask(bits):
        raise ValueError("Значение выходит за размер поля")

def asm_const(B, C):
    """Загрузка константы."""
    check_value(B, 5)
    check_value(C, 15)

    return {"A": 1, "B": B, "C": C}

def asm_read(B, C):
    """Чтение значения из памяти."""
    check_value(B, 5)
    check_value(C, 5)

    return {"A": 5, "B": B, "C": C}


def asm_write(B, C, D):
    """Запись значения в память."""
    check_value(B, 5)
    check_value(C, 9)
    check_value(D, 5)

    return {"A": 0, "B": B, "C": C, "D": D}

def asm_not(B, C):
    """Побитовое НЕ."""
    check_value(B, 5)
    check_value(C, 5)

    return {"A": 15, "B": B, "C": C}

def asm(program):
    """Переводит команды во внутреннее представление."""
    result = []

    for cmd in program:
        op = cmd["op"]

        if op == "load":
            fields = asm_const(cmd["b"], cmd["c"])
        elif op == "read":
            fields = asm_read(cmd["b"], cmd["c"])
        elif op == "write":
            fields = asm_write(cmd["b"], cmd["c"], cmd["d"])
        elif op == "not":
            fields = asm_not(cmd["b"], cmd["c"])
        else:
            raise ValueError(f"Неизвестная команда: {op}")

        result.append(fields)

    return result