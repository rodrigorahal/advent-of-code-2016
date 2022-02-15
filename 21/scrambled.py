import fileinput
from itertools import permutations


def parse():
    operations = []
    for line in fileinput.input():
        operations.append(tuple(map(safe_int, line.strip().split())))
    return operations


def safe_int(value):
    try:
        return int(value)
    except Exception:
        return value


def scramble(seed, operations):
    curr = list(seed)

    for operation in operations:
        name = operation[0]

        if name == "swap":
            type = operation[1]

            if type == "position":
                ix, iy = operation[2], operation[5]
                x, y = curr[ix], curr[iy]
                curr[iy] = x
                curr[ix] = y

            elif type == "letter":
                x, y = operation[2], operation[5]
                ix, iy = curr.index(x), curr.index(y)
                curr[iy] = x
                curr[ix] = y

        elif name == "rotate":
            type = operation[1]

            if type == "left":
                steps = operation[2]
                for _ in range(steps):
                    curr = curr[1:] + [curr[0]]

            elif type == "right":
                steps = operation[2]
                for _ in range(steps):
                    curr = [curr[-1]] + curr[:-1]

            elif type == "based":
                x = operation[-1]
                ix = curr.index(x)
                curr = [curr[-1]] + curr[:-1]
                for _ in range(ix):
                    curr = [curr[-1]] + curr[:-1]
                if ix >= 4:
                    curr = [curr[-1]] + curr[:-1]

        elif name == "reverse":
            lo, hi = operation[2], operation[4]
            letters = curr[lo : hi + 1]
            tmp = curr[:lo] + list(reversed(letters))
            if hi + 1 < len(seed):
                tmp += curr[hi + 1 :]
            curr = tmp

        elif name == "move":
            lo, hi = operation[2], operation[5]
            letter = curr[lo]
            del curr[lo]
            curr.insert(hi, letter)
    return "".join(curr)


def search(seed, operations):
    for candidate in permutations(seed):
        if scramble(candidate, operations) == seed:
            return "".join(candidate)


def main():
    SEED = "abcdefgh"
    operations = parse()

    scrambled = scramble(SEED, operations)
    print(f"Part 1: {scrambled}")

    SEED = "fbgdceah"
    unscrambled = search(SEED, operations)
    print(f"Part 2: {unscrambled}")


if __name__ == "__main__":
    main()
