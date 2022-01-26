import fileinput


def parse():
    return [line.strip() for line in fileinput.input()]


def count(ips, fn):
    return len([ip for ip in ips if fn(ip)])


def is_tls_supported(ip):
    n = len(ip)
    outside = True
    found = False

    for i in range(n - 3):
        a, b, c, d = ip[i], ip[i + 1], ip[i + 2], ip[i + 3]

        if a == "[":
            outside = False
        elif a == "]":
            outside = True

        if (a, b) == (d, c) and a != b:
            if not outside:
                return False
            else:
                found = True
    return found


def is_ssl_supported(ip):
    n = len(ip)
    outside = True
    abas = set()
    babs = set()

    for i in range(n - 2):
        a, b, c = ip[i], ip[i + 1], ip[i + 2]

        if a == "[":
            outside = False
        elif a == "]":
            outside = True

        if a == c and a != b:
            if outside:
                abas.add((a, b, a))
            else:
                babs.add((a, b, a))

    for a, b, _ in abas:
        if (b, a, b) in babs:
            return True

    return False


def main():
    ips = parse()
    print(f"Part 1: {count(ips, is_tls_supported)}")
    print(f"Part 2: {count(ips, is_ssl_supported)}")


if __name__ == "__main__":
    main()
