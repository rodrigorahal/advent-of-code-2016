from hashlib import md5
from random import choice
from string import ascii_lowercase

VALID = list(ascii_lowercase) + list(range(0, 10))


def search(seed, nzeros=5):
    password = ""
    idx = 0
    while len(password) < 8:
        hashed = md5(f"{seed}{idx}".encode("ascii")).hexdigest()
        if hashed.startswith("0" * nzeros):
            password += hashed[5]
        idx += 1
    return password


def search_with_position(seed, nzeros=5, with_animation=False):
    password = [None] * 8
    idx = 0
    while any(char is None for char in password):
        hashed = md5(f"{seed}{idx}".encode("ascii")).hexdigest()
        if hashed.startswith("0" * nzeros):
            if (
                hashed[5].isdigit()
                and 0 <= int(hashed[5]) <= 7
                and password[int(hashed[5])] is None
            ):
                pos, val = int(hashed[5]), hashed[6]
                password[pos] = val
        if with_animation:
            animate(password, idx)
        idx += 1
    return "".join(password)


def animate(password, idx):
    if idx % 50_000 == 0:
        for char in password:
            if char is None:
                print(choice(VALID), end="")
            else:
                print(char, end="")
        print("\r", end="")


def main():
    SEED = "reyedfim"
    print(f"Part 1: {search(SEED)}")
    print(f"Part 2: {search_with_position(SEED, with_animation=True)}")


if __name__ == "__main__":
    main()
