from hashlib import md5
from collections import deque

OPEN = ("b", "c", "d", "e", "f")


def search(seed, start, target):
    queue = deque([])
    queue.append((start, "", 0))
    seen = set()
    solutions = []

    while queue:
        (row, col), path, steps = queue.popleft()
        if path in seen:
            continue
        if (row, col) == target:
            solutions.append(path)
            continue
        seen.add(path)
        is_open = doors(seed, path)
        for (nrow, ncol), ndir in neighbors(row, col, 4, 4):
            if is_open[ndir] and path + ndir not in seen:
                queue.append(((nrow, ncol), path + ndir, steps + 1))
    return min(solutions, key=len), len(max(solutions, key=len))


def doors(seed, path):
    data = f"{seed}{path}"
    hash = md5(data.encode("ascii")).hexdigest()[:4]
    return dict((dir, char in OPEN) for dir, char in zip(["U", "D", "L", "R"], hash))


def neighbors(row, col, height, width):
    for r, c, dir in [(-1, 0, "U"), (0, 1, "R"), (1, 0, "D"), (0, -1, "L")]:
        if 0 <= row + r < height and 0 <= col + c < width:
            yield (row + r, col + c), dir


def main():
    SEED = "edjrjqaa"
    path, steps = search(SEED, (0, 0), (3, 3))
    print(f"Part 1: {path}")
    print(f"Part 2: {steps}")


if __name__ == "__main__":
    main()
