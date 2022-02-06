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
    i = 0
    size = len(tape)
    while i < size:
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

        i += 1
    return mem


def safe_int(w):
    try:
        return int(w)
    except ValueError:
        return w


def main():
    tape = parse()
    mem = {"a": 0, "b": 0, "c": 0, "d": 0}
    run(tape, mem)
    print(f"Part 1: {mem['a']}")
    mem = {"a": 0, "b": 0, "c": 1, "d": 0}
    run(tape, mem)
    print(f"Part 2: {mem['a']}")


if __name__ == "__main__":
    main()
