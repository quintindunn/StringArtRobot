ROWS = 4
COLUMNS = 20


TMP_BUFFER = [""]*ROWS


def clear():
    for i in range(ROWS):
        TMP_BUFFER[i] = ""


def display_line(idx: int, content: str):
    TMP_BUFFER[idx] = content[:COLUMNS]


def display_final():
    print(*TMP_BUFFER, sep="\n")
    print("\n"*3)