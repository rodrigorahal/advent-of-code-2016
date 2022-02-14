from __future__ import annotations
from dataclasses import dataclass


@dataclass
class Elf:
    id: int
    next: Elf
    prev: Elf
    gifts: int


def make(size):
    head = Elf(id=1, next=None, prev=None, gifts=1)
    curr = head
    for i in range(2, size + 1):
        nxt = Elf(id=i, next=None, prev=None, gifts=1)
        curr.next = nxt
        nxt.prev = curr
        curr = nxt
    curr.next = head
    head.prev = curr
    return head


def display(head, size):
    curr = head
    for _ in range(1, size + 1):
        print(curr)
        curr = curr.next


def play(head: Elf, size: int):
    curr = head
    n = size

    while n != 1:
        nxt = curr.next
        curr.gifts += nxt.gifts
        curr.next = nxt.next
        n -= 1
        curr = curr.next

    return curr.id


def play_across(head: Elf, size: int):
    curr = head
    n = size
    across = get_acrros(curr, n)
    while n != 1:
        if n % 2 == 0:
            across = across.next
        curr.gifts += across.gifts
        nxt_across = across.next
        # delete across
        across.prev.next = across.next
        across.next.prev = across.prev
        # update across
        across = nxt_across
        n -= 1
        curr = curr.next
    return curr.id


def get_acrros(head: Elf, n: int):
    curr = head
    for _ in range(n // 2):
        curr = curr.next
    return curr


def main():
    SIZE = 3017957
    head = make(SIZE)
    winner = play(head, SIZE)
    print(f"Part 1: {winner}")

    head = make(SIZE)
    winner = play_across(head, SIZE)
    print(f"Part 2: {winner}")

    # winner = run(SIZE, across=True)
    # # print(f"Part 2: {winner}")

    # # print(next_elf({2: 1, 3: 1, 10: 2}, 2, 10))

    # elfs = make(SIZE)

    # # display(elfs, SIZE)
    # # elf = play(elfs, SIZE)
    # # print(elf)

    # elf = play_across(elfs, SIZE)
    # print(elf)


if __name__ == "__main__":
    main()
