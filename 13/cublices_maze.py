from collections import deque


def cubicle(row, col, seed):
    y = row
    x = col
    res = x * x + 3 * x + 2 * x * y + y + y * y + seed
    bits = bin(res).count("1")
    return "." if bits % 2 == 0 else "#"


def neighbors(row, col):
    for dr in [-1, 0, 1]:
        for dc in [-1, 0, 1]:
            if abs(dr) != abs(dc) and 0 <= row + dr and 0 <= col + dc:
                yield row + dr, col + dc


def search(start, target, seed):
    queue = deque([])
    queue.append((start, 0))
    seen = dict()

    while queue:
        (row, col), steps = queue.popleft()

        if (row, col) in seen:
            continue

        seen[(row, col)] = steps

        if (row, col) == target:
            break

        for nrow, ncol in neighbors(row, col):
            if cubicle(nrow, ncol, seed) == "." and (nrow, ncol) not in seen:
                queue.append(((nrow, ncol), steps + 1))
    return seen[target], sum(steps <= 50 for steps in seen.values())


def display_grid(H, W, seed):
    for row in range(H):
        print("".join(cubicle(row, col, seed) for col in range(W)))
    print()


def main():
    SEED = 1362
    steps, positions = search((1, 1), (39, 31), SEED)
    print(f"Part 1: {steps}")

    print(f"Part 2: {positions}")


if __name__ == "__main__":
    main()
