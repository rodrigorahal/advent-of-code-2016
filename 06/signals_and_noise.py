import fileinput
from collections import defaultdict, Counter


def parse():
    return [line.strip() for line in fileinput.input()]


def decode(messages, least=False):
    freqs = defaultdict(Counter)

    for message in messages:
        for i, char in enumerate(message):
            freqs[i][char] += 1

    idx = -1 if least else 0

    return "".join(
        counter.most_common()[idx][0] for _, counter in sorted(freqs.items())
    )


def main():
    messages = parse()
    decoded = decode(messages)
    print(f"Part 1: {decoded}")
    decoded = decode(messages, least=True)
    print(f"Part 1: {decoded}")


if __name__ == "__main__":
    main()
