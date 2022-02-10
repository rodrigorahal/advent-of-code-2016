def dragon(seed, size):
    return checksum(generate(seed, size))


def generate(data, size):
    current = data
    while len(current) < size:
        current = step(current)
    return current[:size]


def step(current):
    a = current
    b = "".join("1" if char == "0" else "0" for char in reversed(current))
    return f"{a}0{b}"


def checksum(data):
    current = data
    n = len(current)
    while n % 2 == 0:
        current = stepcheck(current)
        n = len(current)
    return current


def stepcheck(data):
    current = data
    n = len(current)
    i = 0
    next = []
    while i < n - 1:
        a, b = current[i], current[i + 1]
        i += 2
        if a == b:
            next.append("1")
        else:
            next.append("0")
    return "".join(next)


def main():
    SEED = "01111010110010011"
    print(f"Part 1: {dragon(SEED, 272)}")
    print(f"Part 2: {dragon(SEED, 35651584)}")


if __name__ == "__main__":
    main()
