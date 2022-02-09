import fileinput
from functools import cache


def parse():
    discs = []
    for line in fileinput.input():
        words = line.strip().strip(".").split()
        positions, start = tuple(map(int, (words[3], words[-1])))
        discs.append((positions, start))
    return discs


def search(discs):
    time = 0
    while True:
        if all(position(disc, time + t) == 0 for t, disc in enumerate(discs, start=1)):
            break
        time += 1
    return time


@cache
def position(disc, time):
    positions, start = disc
    return (start + (time % positions)) % positions


def main():
    discs = parse()
    time = search(discs)
    print(f"Part 1: {time}")

    discs.append((11, 0))
    time = search(discs)
    print(f"Part 2: {time}")


if __name__ == "__main__":
    main()
