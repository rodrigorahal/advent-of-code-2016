import fileinput
from collections import deque


def parse():
    grid = []
    start = None
    targets = []
    for r, line in enumerate(fileinput.input()):
        row = []
        for c, val in enumerate(line.strip()):
            if val.isdigit():
                if val != "0":
                    targets.append((r, c))
                else:
                    start = (r, c)
            row.append(val)
        grid.append(row)
    return grid, start, targets


def display(grid):
    for row in grid:
        print("".join(val for val in row))
    print()


def neighbors(grid, row, col):
    H = len(grid)
    W = len(grid[0])

    for dr in [-1, 0, 1]:
        for dc in [-1, 0, 1]:
            if abs(dr) == abs(dc):
                continue

            if 0 <= row + dr < H and 0 <= col + dc < W:
                yield row + dr, col + dc


def search(grid, start, targets, with_return=False):
    queue = deque([])
    queue.append((start, 0, set()))

    visited = set()

    while queue:
        (row, col), steps, seen = queue.popleft()

        if ((row, col), tuple(seen)) in visited:
            continue

        visited.add(((row, col), tuple(seen)))

        if with_return:
            if len(seen.intersection(targets)) == len(targets) and (row, col) == start:
                return steps
        elif len(seen.intersection(targets)) == len(targets):
            return steps

        for nrow, ncol in neighbors(grid, row, col):
            if grid[nrow][ncol] == "#":
                continue
            updated_seen = (
                {*seen} | {(nrow, ncol)} if grid[nrow][ncol].isdigit() else {*seen}
            )
            queue.append(((nrow, ncol), steps + 1, updated_seen))


def main():
    grid, start, targets = parse()

    steps = search(grid, start, set(targets))
    print(f"Part 1 :{steps}")

    steps = search(grid, start, set(targets), with_return=True)
    print(f"Part 2: {steps}")


if __name__ == "__main__":
    main()
