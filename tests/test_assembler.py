from src.assembler import asm_const
from src.assembler import asm_read
from src.assembler import asm_write
from src.assembler import asm_not
from src.assembler import asm

def practice():
    assert asm_const(17, 551) == {
        "A": 1, "B": 17, "C": 551
    }

    assert asm_read(15, 5) == {
        "A": 5, "B": 15, "C": 5
    }

    assert asm_write(24, 13, 11) == {
        "A": 0, "B": 24, "C": 13, "D": 11
    }

    assert asm_not(0, 8) == {
        "A": 15, "B": 0, "C": 8
    }

    program = [
        {"op": "load", "b": 17, "c": 551},
        {"op": "read", "b": 15, "c": 5},
        {"op": "write", "b": 24, "c": 13, "d": 11},
        {"op": "not", "b": 0, "c": 8}
    ]

    result = asm(program)

    assert len(result) == 4
    assert result[0]["A"] == 1
    assert result[1]["A"] == 5
    assert result[2]["A"] == 0
    assert result[3]["A"] == 15

    print("Все тесты пройдены")

if __name__ == "__main__":
    practice()