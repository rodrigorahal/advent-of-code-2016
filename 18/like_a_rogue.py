import fileinput


def parse():
    line = fileinput.input().readline().strip()
    return ["."] + [char for char in line] + ["."]


def generate(row, size):
    grid = [row]
    while len(grid) < size:
        row = grid[-1]
        grid.append(next(row))
    return grid


def next(row):
    new = []
    n = len(row)
    for i in range(1, n - 1):
        left, center, right = row[i - 1], row[i], row[i + 1]
        if left == center == "^" and right == ".":
            new.append("^")
        elif center == right == "^" and left == ".":
            new.append("^")
        elif left == "^" and center == right == ".":
            new.append("^")
        elif right == "^" and left == center == ".":
            new.append("^")
        else:
            new.append(".")
    return ["."] + new + ["."]


def count(grid):
    safe = 0
    for row in grid:
        for tile in row[1:-1]:
            if tile == ".":
                safe += 1
    return safe


def display(grid):
    for row in grid:
        print("".join(tile for tile in row[1:-1]))
    print()


def main():
    SIZE = 40
    row = parse()
    grid = generate(row, SIZE)
    print(f"Part 1: {count(grid)}")
    SIZE = 400000
    grid = generate(row, SIZE)
    print(f"Part 2: {count(grid)}")


if __name__ == "__main__":
    main()
