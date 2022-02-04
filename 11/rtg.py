import json
from itertools import combinations
from hashlib import md5
import heapq


def search(initial_state):
    queue = []
    heapq.heappush(queue, (distance(initial_state), 0, initial_state.items(), 1))
    seen = dict()

    while queue:
        _, steps, state, elevator = heapq.heappop(queue)
        state = dict(state)
        hashed = hash(state, elevator)

        if hashed in seen and seen[hashed] <= steps:
            continue

        seen[hashed] = steps

        if is_solution(state, elevator):
            # greedy heauristic seems to work
            return steps

        for next_state, next_elevator in next_states(state, elevator):
            heapq.heappush(
                queue,
                (
                    distance(next_state),
                    steps + 1,
                    next_state.items(),
                    next_elevator,
                ),
            )

    return -1


def is_solution(state, elevator):
    if (
        elevator == 4
        and all(len(state[floor]) == 0 for floor in [1, 2, 3])
        and len(state[elevator]) != 0
    ):
        return True
    return False


def distance(state):
    dist = 0
    for floor, items in state.items():
        dist += (4 - floor) * len(items)
    return dist


def next_states(state, elevator):
    floor = elevator
    upper = floor + 1
    lower = floor - 1

    for items in list(combinations(state[floor], 2)) + list(
        combinations(state[floor], 1)
    ):
        if 2 <= upper <= 4:
            new_state = generate_new_state(state, floor, upper, items)
            if is_safe(new_state, floor) and is_safe(new_state, upper):
                yield [new_state, elevator + 1]
        if 1 <= lower <= 3:
            new_state = generate_new_state(state, floor, lower, items)
            if is_safe(new_state, floor) and is_safe(new_state, lower):
                yield [new_state, elevator - 1]


def generate_new_state(state, from_floor, to_floor, to_move):
    return {
        **state,
        to_floor: state[to_floor] + [*to_move],
        from_floor: [item for item in state[from_floor] if item not in to_move],
    }


def hash(state, elevator):
    data = {
        "E": elevator,
        **{str(k): sorted(v) for k, v in equivalent(state).items()},
    }

    return md5(json.dumps(data, sort_keys=True).encode("utf-8")).hexdigest()


def is_safe(state, floor):
    items = state[floor]

    generators = set(item for item in items if item[-1] == "G")
    chips = set(item for item in items if item[-1] == "M")

    if not chips:
        return True

    if not generators:
        return True

    for chip in chips:
        pair = chip[:-1] + "G"
        if pair not in generators:
            return False

    return True


def equivalent(state):
    eqstate = dict()
    for idx, floor in state.items():
        generators = set(item for item in floor if item[-1] == "G")
        chips = set(item for item in floor if item[-1] == "M")

        pairs = set()

        for item in chips:
            pair = item[:-1] + "G"
            if pair in generators:
                pairs.add((item, pair))

        for chip, gen in pairs:
            chips.remove(chip)
            generators.remove(gen)

        res = []
        if pairs:
            res.append(str(len(pairs)))
        for c in chips:
            res.append(c)
        for g in generators:
            res.append(g)

        eqstate[idx] = res

    return eqstate


def main():
    TEST_STATE = {
        4: [],
        3: ["LIG"],
        2: ["HIG"],
        1: ["HIM", "LIM"],
    }

    STATE = {
        4: [],
        3: [],
        2: ["POM", "PRM"],
        1: ["POG", "THG", "THM", "PRG", "RUG", "RUM", "COG", "COM"],
    }

    steps = search(STATE)
    print(f"Part 1: {steps}")

    STATE = {
        4: [],
        3: [],
        2: ["POM", "PRM"],
        1: [
            "POG",
            "THG",
            "THM",
            "PRG",
            "RUG",
            "RUM",
            "COG",
            "COM",
            "ELG",
            "ELM",
            "DIG",
            "DIM",
        ],
    }

    steps = search(STATE)
    print(f"Part 2: {steps}")


if __name__ == "__main__":
    main()
