from dis import dis
import fileinput
from copy import deepcopy
from turtle import st
from xxlimited import new


def parse():
    instructions = []
    for line in fileinput.input():
        words = line.strip().split()
        if len(words) == 2:
            cmd = words[0]
            w, h = tuple(map(int, words[1].split("x")))
            instructions.append((cmd, w, h))
        else:
            cmd = words[0]
            orientation = words[1]
            axis = int(words[2].split("=")[-1])
            by = int(words[-1])
            instructions.append((cmd, orientation, axis, by))
    return instructions


def apply(grid, instructions):
    H = len(grid)
    W = len(grid[0])
    state = deepcopy(grid)
    for instruction in instructions:
        new_state = deepcopy(state)
        cmd = instruction[0]

        if cmd == "rect":
            _, w, h = instruction
            for row in range(h):
                for col in range(w):
                    new_state[row][col] = "#"

        elif cmd == "rotate":
            _, orientation, axis, by = instruction

            if orientation == "column":
                for row in range(H):
                    new_state[(row + by) % H][axis] = state[row][axis]

            elif orientation == "row":
                for col in range(W):
                    new_state[axis][(col + by) % W] = state[axis][col]
        state = new_state
    return state


def make_grid(width, height):
    grid = []
    for _ in range(height):
        grid.append(["." for _ in range(width)])
    return grid


def display(grid):
    for row in grid:
        print(" ".join(val if val == "#" else " " for val in row))
    print()
    return


def lit(grid):
    return sum(val == "#" for row in grid for val in row)


def main():
    instructions = parse()
    grid = make_grid(50, 6)
    state = apply(grid, instructions)
    print(f"Part 1: {lit(state)}")
    print("Part 2:")
    display(state)


if __name__ == "__main__":
    main()
