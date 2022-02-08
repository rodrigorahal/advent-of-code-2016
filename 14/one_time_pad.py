from hashlib import md5
from collections import defaultdict


def generate(salt, stretch=False):
    candidates_by_repeat = defaultdict(list)
    keys = set()

    idx = 0
    while len(keys) < 64:
        seed = f"{salt}{idx}"
        if stretch:
            hash = stretched(seed)
        else:
            hash = md5(seed.encode("ascii")).hexdigest()
        three_repeat = has_repeat(hash, size=3)
        if three_repeat:
            candidates_by_repeat[three_repeat].append((idx, hash))

        five_repeats = has_repeat(hash, size=5)
        if five_repeats:
            five_repeat = five_repeats
            candidates = []
            for candidate_idx, candidate_hash in candidates_by_repeat[five_repeat]:
                if idx == candidate_idx:
                    candidates.append((candidate_idx, candidate_hash))
                elif idx - candidate_idx <= 1000:
                    keys.add((candidate_idx, candidate_hash))
            candidates_by_repeat[five_repeat] = candidates

        idx += 1

    return sorted(keys)[63][0]


def has_repeat(hash, size):
    n = len(hash)
    for i in range(n - (size - 1)):
        window = hash[i : i + size]
        if len(set(window)) == 1:
            return window[0]
    return False


def stretched(seed):
    hash = md5(seed.encode("ascii")).hexdigest()
    for i in range(2016):
        hash = md5(hash.encode("ascii")).hexdigest()
    return hash


def main():
    SALT = "ihaygndm"
    key = generate(SALT)
    print(f"Part 1: {key}")

    key = generate(SALT, stretch=True)
    print(f"Part 2: {key}")


if __name__ == "__main__":
    main()
