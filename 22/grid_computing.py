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
    r = []
    for dr in [-1, 0, 1]:
        for dc in [-1, 0, 1]:
            if (
                abs(dr) != abs(dc)
                and 0 <= col + dc <= width
                and 0 <= row + dr <= height
            ):
                r.append((row + dr, col + dc))
    return r


def free(state, row, col, H, W, seen=None, steps=0):
    if not seen:
        seen = set()

    seen.add((row, col))

    moves = []
    a = state[row][col]

    # print(f"Freeing {row},{col}")
    for nrow, ncol in neighbors(row, col, H, W):
        b = state[nrow][ncol]
        # print(f"Trying {nrow},{ncol}")
        if (nrow, ncol) in seen:
            # print(f"Seen {nrow},{ncol}")
            continue
        elif can_move(a, b):
            # print(f"Can move to {nrow},{ncol}")
            moves.append((move(state, a, b), steps + 1))
        elif is_possible_if_free(a, b):
            deep_moves = free(state, nrow, ncol, H, W, seen, steps)
            # print(f"At: {row,col} Deep moves from {nrow,ncol}: {len(deep_moves)}")
            for deep_state, deep_steps in deep_moves:
                # print("Deep state")
                # display(deep_state)
                if can_move(deep_state[row][col], deep_state[nrow][ncol]):
                    moves.append(
                        (
                            move(
                                deep_state, deep_state[row][col], deep_state[nrow][ncol]
                            ),
                            steps + deep_steps + 1,
                        )
                    )
    # print(f"Returning from {row},{col}: {len(moves)}")
    return moves


def move(state: List[List[Node]], a: Node, b: Node):
    moved_state = deepcopy(state)
    row, col = a.position
    nrow, ncol = b.position

    moved_state[row][col] = Node(
        id=a.id,
        size=a.size,
        used=0,
        avail=a.size,
        use=0,
        position=a.position,
    )

    moved_state[nrow][ncol] = Node(
        id=b.id,
        size=b.size,
        used=a.used + b.used,
        avail=b.avail - a.used,
        use=b.used,
        position=b.position,
    )
    return moved_state


def search(grid, start, target):
    H = len(grid) - 1
    W = len(grid[0]) - 1

    queue = deque()
    queue.append((grid, start, 0, set()))

    seen_states = set()

    min_steps = None

    while queue:
        state, (row, col), steps, seen = queue.popleft()

        # if (row, col) in seen_states:
        #     continue

        hashed = _hash(state, (row, col))

        if hashed in seen_states:
            continue

        seen_states.add(hashed)

        print(f"we are at: {row,col}")

        if min_steps and steps > min_steps:
            continue

        if (row, col) == target:
            if not min_steps:
                min_steps = steps
            else:
                if steps < min_steps:
                    min_steps = steps
            continue

        print(f"--------------- {min_steps} ----------")

        a = state[row][col]

        for nrow, ncol in neighbors(row, col, len(grid) - 1, len(grid[0]) - 1):
            if (nrow, ncol) in seen:
                continue
            b = state[nrow][ncol]
            if can_move(a, b):
                queue.append(
                    (
                        move(state, a, b),
                        b.position,
                        steps + 1,
                        {*seen} | {a.position},
                    )
                )
            elif is_possible_if_free(a, b):
                deep_states = free(state, nrow, ncol, H, W, {a.position})
                if deep_states:
                    ss = sorted(deep_states, key=itemgetter(1))
                    deep_state, deep_steps = ss[0]

                    # for deep_state, deep_steps in deep_states:
                    queue.append(
                        (
                            move(
                                deep_state, deep_state[row][col], deep_state[nrow][ncol]
                            ),
                            b.position,
                            steps + deep_steps + 1,
                            {*seen} | {a.position},
                        )
                    )
        queue = deque(sorted(queue, key=itemgetter(2, 1)))
    return min_steps


def _hash(state, curr):
    flat = [curr]
    for row in state:
        for node in row:
            flat.append((node.id, node.used, node.size))
    return tuple(flat)


def to_grid(nodes_by_position, H, W):
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


def bfs(grid, start, target):
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
            return steps

        a = grid[row][col]

        for nrow, ncol in neighbors(row, col, H, W):
            b = grid[nrow][ncol]
            if is_possible_if_free(a, b):
                queue.append(((nrow, ncol), steps + 1))


def calculate(steps, W):
    return steps + 1 + (W - 1) * 5


def main():
    nodes = parse()
    pairs = viable(nodes)
    print(f"Part 1: {len(pairs)}")

    node_by_position = dict((node.position, node) for node in nodes)

    H, W = dimensions(nodes)
    print(H, W)

    SWAP = swap_disk(pairs)
    print(SWAP)

    grid = to_grid(node_by_position, H + 1, W + 1)

    s = bfs(grid, start=SWAP.position, target=(0, W - 1))
    print(s)
    print(calculate(s, W))


if __name__ == "__main__":
    main()
