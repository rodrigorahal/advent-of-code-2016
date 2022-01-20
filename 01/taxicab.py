import fileinput


def parse():
    return [
        (direction[0], int(direction[1:]))
        for direction in fileinput.input().readline().strip().split(", ")
    ]


def walk(directions):
    X, Y = 0, 1
    x, y = 0, 0

    for dir, amt in directions:
        X, Y = turn(X, Y, dir)
        x += X * amt
        y += Y * amt
    return abs(x) + abs(y)


def walk_with_tracking(directions):
    X, Y = 0, 1
    x, y = 0, 0

    seen = set([(0, 0)])

    for dir, amt in directions:
        X, Y = turn(X, Y, dir)
        next_x = x + (X * amt)
        next_y = y + (Y * amt)

        for bx, by in blocks((x, y), (next_x, next_y)):
            if (bx, by) in seen and (bx, by) != (x, y):
                return abs(bx) + abs(by)
            seen.add((bx, by))

        x = next_x
        y = next_y

    return -1


def turn(X, Y, dir):
    if dir == "L":
        return (-Y, X)
    elif dir == "R":
        return (Y, -X)


def blocks(current, final):
    x, y = current
    next_x, next_y = final
    if x != next_x:
        lo, hi = sorted([x, next_x])
        diff = 1 if hi >= 1 else 0
        for i in range(lo, hi + diff):
            yield (i, y)

    elif y != next_y:
        lo, hi = sorted([y, next_y])
        diff = 1 if hi > 1 else 0
        for j in range(lo, hi + diff):
            yield (x, j)


def main():
    directions = parse()
    distance = walk(directions)
    print(f"Part 1: {distance}")

    distance = walk_with_tracking(directions)
    print(f"Part 2: {distance}")


if __name__ == "__main__":
    main()
