import fileinput


def parse():
    candidates = []
    for line in fileinput.input():
        candidates.append(tuple(map(int, line.strip().split())))
    return candidates


def count(candidates):
    return sum(is_valid(candidate) for candidate in candidates)


def count_vertical(candidates):
    return sum(
        is_valid(candidate)
        for row in range(0, len(candidates) - 2, 3)
        for candidate in zip(candidates[row], candidates[row + 1], candidates[row + 2])
    )


def is_valid(candidate):
    a, b, c = sorted(candidate)
    return a + b > c


def main():
    candidates = parse()
    print(f"Part 1: {count(candidates)}")
    print(f"Part 2: {count_vertical(candidates)}")


if __name__ == "__main__":
    main()
