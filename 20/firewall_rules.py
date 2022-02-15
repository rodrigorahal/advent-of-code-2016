import fileinput
from itertools import pairwise
from unittest import result


def parse():
    blocked = []
    for line in fileinput.input():
        interval = tuple(map(int, line.strip().split("-")))
        blocked.append(interval)
    return sorted(blocked)


def search(blocked):
    for (s, e), (ns, ne) in pairwise(blocked):
        if ns - e > 1:
            return e + 1


def count(normalized):
    allowed = 0
    for (s, e), (ns, ne) in pairwise(normalized):
        if ns - e > 1:
            allowed += ns - e - 1
    s, e = normalized[-1]
    if e != 2 ** 32:
        allowed += 2 ** 32 - e - 1
    return allowed


def normalize(blocked):
    normalized = [blocked[0]]
    for interval in blocked[1:]:
        normalized = merged(normalized, interval)
    return normalized


def merged(blocked, candidate):
    updated = []
    for interval in blocked:
        if interval == candidate:
            continue
        result = merge(candidate, interval)
        if result:
            updated.append(result)
            break
        else:
            updated.append(interval)
    else:
        updated.append(candidate)

    return updated


def merge(a, b):
    """
    s---------e
    |         |   ns---------ne
    |   ns----|-------ne
    | ns---ne |
    """
    (s, e), (ns, ne) = sorted([a, b])
    if ns > e + 1:
        return None
    if s <= ns <= e + 1 and ne > e:
        return s, ne
    if s <= ns <= e + 1 and s <= ne <= e:
        return s, e


def main():
    blocked = parse()
    least = search(blocked)
    print(f"Part 1: {least}")
    normalized = sorted(normalize(blocked))
    print(f"Part 2: {count(normalized)}")


if __name__ == "__main__":
    main()
