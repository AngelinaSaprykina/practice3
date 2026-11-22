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

def encode_const(B, C):
    """Переводит загрузку константы в байты"""
    cmd = 1
    cmd |= (B & mask(5)) << 4
    cmd |= (C & mask(15)) << 9
    return cmd.to_bytes(3, "little")

def encode_read(B, C):
    """Переводит чтение из памяти в байты"""
    cmd = 5
    cmd |= (B & mask(5)) << 4
    cmd |= (C & mask(5)) << 9
    return cmd.to_bytes(3, "little")

def encode_write(B, C, D):
    """Переводит запись в память в байты"""
    cmd = 0
    cmd |= (B & mask(5)) << 4
    cmd |= (C & mask(9)) << 9
    cmd |= (D & mask(5)) << 18
    return cmd.to_bytes(3, "little")

def encode_not(B, C):
    """Переводит побитовое НЕ в байты"""
    cmd = 15
    cmd |= (B & mask(5)) << 4
    cmd |= (C & mask(5)) << 9
    return cmd.to_bytes(3, "little")

def asm_bytes(program):
    """Переводит промежуточное представление в машинный код"""
    result = b""

    for cmd in program:
        if cmd["A"] == 1:
            result += encode_const(cmd["B"], cmd["C"])

        if cmd["A"] == 5:
            result += encode_read(cmd["B"], cmd["C"])

        if cmd["A"] == 0:
            result += encode_write(
                cmd["B"], cmd["C"], cmd["D"]
            )

        if cmd["A"] == 15:
            result += encode_not(cmd["B"], cmd["C"])

    return result