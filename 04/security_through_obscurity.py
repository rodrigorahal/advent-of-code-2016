import fileinput
from collections import Counter


def parse():
    rooms = []
    for line in fileinput.input():
        content = line.strip().split("-")
        name, rest = content[:-1], content[-1]
        code, checksum = rest.strip("]").split("[")
        code = int(code)
        rooms.append((name, code, checksum))
    return rooms


def filter(rooms):
    return [
        (name, code, checksum)
        for (name, code, checksum) in rooms
        if most_common_in(name) == checksum
    ]


def search(rooms):
    for name, code, _ in rooms:
        decoded = decode(name, code)
        if "north" in decoded:
            return (decoded, code)


def decode(name, code):
    shift = code % 26
    decoded = []
    for word in name:
        decoded_word = []
        for char in word:
            if ord(char) + shift > 122:
                decoded_char = chr(ord(char) + shift - 122 + 96)
            else:
                decoded_char = chr(ord(char) + shift)
            decoded_word.append(decoded_char)
        decoded.append("".join(decoded_word))
    return " ".join(decoded)


def most_common_in(name):
    counter = Counter([char for word in name for char in word])
    items = sorted(counter.items(), key=lambda item: (-item[1], item[0]))
    return "".join([k for k, _ in items])[:5]


def main():
    rooms = parse()
    valid = filter(rooms)
    print(f"Part 1: {sum(code for _, code, _ in valid)}")
    name, code = search(valid)
    print(f"Part 2: {name}: {code}")


if __name__ == "__main__":
    main()
