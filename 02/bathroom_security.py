import fileinput

BUTTONS = [
    [1, 2, 3],
    [4, 5, 6],
    [7, 8, 9],
]

KEYPAD = [
    [0, 0, 1, 0, 0],
    [0, 2, 3, 4, 0],
    [5, 6, 7, 8, 9],
    [0, "A", "B", "C", 0],
    [0, 0, "D", 0, 0],
]


def parse():
    return [line.strip() for line in fileinput.input()]


def follow(instructions, buttons, start=(1, 1)):
    code = []
    row, col = start
    for instruction in instructions:
        for direction in instruction:
            adj = adjacent(buttons, row, col, direction)
            if adj:
                row, col = adj[0], adj[1]
        code.append(buttons[row][col])
    return "".join(str(n) for n in code)


def adjacent(buttons, row, col, direction):
    h = len(buttons)
    w = len(buttons[0])

    if direction == "U":
        nxt_row, nxt_col = row - 1, col
    elif direction == "R":
        nxt_row, nxt_col = row, col + 1
    elif direction == "D":
        nxt_row, nxt_col = row + 1, col
    elif direction == "L":
        nxt_row, nxt_col = row, col - 1

    if 0 <= nxt_row < h and 0 <= nxt_col < w:
        if buttons[nxt_row][nxt_col] != 0:
            return nxt_row, nxt_col
    return None


def main():
    instructions = parse()
    code = follow(instructions, BUTTONS)
    print(f"Part 1: {code}")

    code = follow(instructions, KEYPAD, start=(2, 0))
    print(f"Part 2: {code}")


if __name__ == "__main__":
    main()
