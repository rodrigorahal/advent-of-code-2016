import fileinput
import heapq
from collections import defaultdict, deque
from copy import deepcopy
from dataclasses import dataclass
from operator import itemgetter
from typing import List, Tuple
from itertools import combinations


@dataclass(eq=True, frozen=True)
class Node:
    id: str
    size: int
    used: int
    avail: int
    use: int
    position: Tuple[int]


def parse():
    nodes = []
    for i, line in enumerate(fileinput.input()):
        if i in (0, 1):
            continue
        words = line.strip().split()
        id = words[0]
        x, y = id.split("/")[-1].split("-")[1:]
        x, y = int(x[1:]), int(y[1:])
        size, used, avail, use = words[1:]
        nodes.append(
            Node(
                id=id,
                size=int(size[:-1]),
                used=int(used[:-1]),
                avail=int(avail[:-1]),
                use=int(use[:-1]),
                position=(y, x),  # x -> col, y -> row
            )
        )
    return nodes


def viable(nodes: List[Node]) -> Tuple[Node, Node]:
    pairs = []
    for a, b in combinations(nodes, 2):
        if can_move(a, b):
            pairs.append((a, b))
        elif can_move(b, a):
            pairs.append((b, a))
    return pairs


def can_move(a: Node, b: Node):
    if a.used != 0 and a.id != b.id and a.used <= b.avail:
        return True
    return False


def is_possible_if_free(a: Node, b: Node):
    return a.used <= b.size


def dimensions(nodes: List[Node]):
    H = max(node.position[0] for node in nodes)
    W = max(node.position[1] for node in nodes)
    return H, W


def neighbors(row, col, height, width):
    result = []
    for dr in [-1, 0, 1]:
        for dc in [-1, 0, 1]:
            if (
                abs(dr) != abs(dc)
                and 0 <= col + dc <= width
                and 0 <= row + dr <= height
            ):
                result.append((row + dr, col + dc))
    return result


def to_grid(nodes, H, W):
    nodes_by_position = dict((node.position, node) for node in nodes)
    grid = []
    for r in range(H):
        row = []
        for c in range(W):
            row.append(nodes_by_position[(r, c)])
        grid.append(row)
    return grid


def display(grid: List[List[Node]]):
    for row in grid:
        print(" ".join(f"{node.used:03}/{node.size:03}" for node in row))
    print()


def to_file(grid: List[List[Node]]):
    with open("out.txt", "w") as f:
        for row in grid:
            line = " ".join(
                f"{node.used if node.used <= 100 else '#'}/{node.size}" for node in row
            )
            f.write(f"{line}\n")


def swap_disk(pairs: Tuple[Node, Node]) -> Node:
    pairs_by_origin = defaultdict(list)
    for a, b in pairs:
        pairs_by_origin[a.position].append(b)
        destinations = set()
    for k, v in pairs_by_origin.items():
        for n in v:
            destinations.add(n)
    assert len(destinations) == 1
    return next(iter(destinations))


def search(grid, start, target):
    H = len(grid) - 1
    W = len(grid[0]) - 1

    queue = deque([])
    queue.append((start, 0))
    seen = set()

    while queue:
        (row, col), steps = queue.popleft()

        if (row, col) in seen:
            continue

        seen.add((row, col))

        if (row, col) == target:
            break

        a = grid[row][col]

        for nrow, ncol in neighbors(row, col, H, W):
            b = grid[nrow][ncol]
            if is_possible_if_free(a, b):
                queue.append(((nrow, ncol), steps + 1))

    # move swap disk to the right of target node
    # perform a 5-step cycle to get target to 0,0 (W-1) times
    return steps + 1 + (W - 1) * 5


def calculate(steps, W):
    return steps + 1 + (W - 1) * 5


def main():
    nodes = parse()
    pairs = viable(nodes)
    print(f"Part 1: {len(pairs)}")
    H, W = dimensions(nodes)
    SWAP = swap_disk(pairs)
    grid = to_grid(nodes, H + 1, W + 1)
    steps = search(grid, start=SWAP.position, target=(0, W - 1))
    print(f"Part 2: {steps}")


if __name__ == "__main__":
    main()
