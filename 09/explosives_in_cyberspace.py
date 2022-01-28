import fileinput


def parse():
    return fileinput.input().readline().strip()


def decompress(contents):
    decompressed = []
    i = 0
    offset = 1
    times = 1
    while i < len(contents):
        if contents[i] == "(":
            offset = []
            i += 1
            while contents[i] != "x":
                offset.append(contents[i])
                i += 1
            offset = int("".join(offset))
            i += 1
            times = []
            while contents[i] != ")":
                times.append(contents[i])
                i += 1
            times = int("".join(times))
            i += 1

            compressed = contents[i : i + offset]
            for _ in range(times):
                decompressed.append(compressed)
            i += offset
            offset = 1
            times = 1

        else:
            compressed = contents[i : i + offset]
            for _ in range(times):
                decompressed.append(compressed)
            i += offset
            offset = 1
            times = 1

    return "".join(decompressed)


def decompressv2(contents, counter=0, upper=1):
    i = 0
    offset = 1
    times = 1
    while i < len(contents):
        if contents[i] == "(":
            offset = []
            i += 1
            while contents[i] != "x":
                offset.append(contents[i])
                i += 1
            offset = int("".join(offset))
            i += 1
            times = []
            while contents[i] != ")":
                times.append(contents[i])
                i += 1
            times = int("".join(times))
            i += 1

            compressed = contents[i : i + offset]
            counter = decompressv2(compressed, counter, times * upper)
            i += offset
            offset = 1
            times = 1

        else:
            compressed = contents[i : i + offset]
            counter += len(compressed) * upper
            i += offset
            offset = 1
            times = 1

    return counter


def main():
    contents = parse()
    decompressed = decompress(contents)
    print(f"Part 1: {len(decompressed)}")
    decompressed = decompressv2(contents)
    print(f"Part 2: {decompressed}")


if __name__ == "__main__":
    main()
