import fileinput


def parse():
    tape = []
    for line in fileinput.input():
        words = line.strip().split()
        if len(words) == 3:
            cmd, x, y = words
            tape.append((cmd, safe_int(x), safe_int(y)))
        else:
            cmd, x = words
            tape.append((cmd, x))
    return tape


def run(tape, mem):
    out = []
    i = 0
    size = len(tape)
    while i < size:
        if len(out) > 100:
            return True

        instruction = tape[i]

        if len(instruction) == 3:
            cmd, x, y = instruction

            if cmd == "cpy":
                if isinstance(x, int):
                    mem[y] = x
                else:
                    mem[y] = mem[x]

            elif cmd == "jnz":
                if isinstance(x, int):
                    if x != 0:
                        i += y
                        continue

                elif mem[x] != 0:
                    i += y
                    continue

        elif len(instruction) == 2:
            cmd, x = instruction

            if cmd == "inc":
                mem[x] += 1

            elif cmd == "dec":
                mem[x] -= 1

            elif cmd == "out":
                if isinstance(x, int):
                    if x not in (0, 1):
                        return False
                    elif out and out[-1] == x:
                        return False
                    out.append(x)
                else:
                    if mem[x] not in (0, 1):
                        return False
                    elif out and out[-1] == mem[x]:
                        return False
                    out.append(mem[x])

        i += 1
    return False


def safe_int(w):
    try:
        return int(w)
    except ValueError:
        return w


def search(tape):
    for i in range(1_000):
        if run(tape, {"a": i, "b": 0, "c": 0, "d": 0}) is True:
            return i


def main():
    tape = parse()
    input = search(tape)
    print(f"Part 1: {input}")


if __name__ == "__main__":
    main()
