import fileinput
from math import factorial


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
                if isinstance(y, int):
                    i += 1
                    continue
                if isinstance(x, int):
                    mem[y] = x
                else:
                    mem[y] = mem[x]

            elif cmd == "jnz":
                if isinstance(x, int):
                    if x != 0:
                        if isinstance(y, int):
                            i += y
                        else:
                            i += mem[y]
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

            elif cmd == "tgl":
                x = safe_int(x)

                if isinstance(x, int):
                    tgl_idx = i + x
                    pass

                else:
                    tgl_idx = i + mem[x]

                if tgl_idx < 0 or tgl_idx >= len(tape):
                    i += 1
                    continue

                to_tgl_instruction = tape[tgl_idx]

                if len(to_tgl_instruction) == 2:
                    tgl_cmd, x = to_tgl_instruction

                    if tgl_cmd == "inc":
                        tape[tgl_idx] = ("dec", x)
                    else:
                        tape[tgl_idx] = ("inc", x)

                elif len(to_tgl_instruction) == 3:
                    tgl_cmd, x, y = to_tgl_instruction

                    if tgl_cmd == "jnz":
                        tape[tgl_idx] = ("cpy", x, y)
                    else:
                        tape[tgl_idx] = ("jnz", x, y)

        i += 1
    return mem


def safe_int(w):
    try:
        return int(w)
    except ValueError:
        return w


def disassembled(a):
    a = factorial(a)
    a += 81 * 94
    return a


def main():
    tape = parse()
    mem = {"a": 7, "b": 0, "c": 0, "d": 0}
    run(tape, mem)
    print(f"Part 1: {mem['a']}")
    print(f"Part 2: {disassembled(12)}")


if __name__ == "__main__":
    main()
