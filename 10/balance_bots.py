import fileinput
from dataclasses import dataclass, field
from math import prod
from typing import Dict, List, Tuple


@dataclass
class Bot:
    id: int
    values: List[int] = field(default_factory=list)

    @property
    def low(self):
        if self.values and len(self.values) == 2:
            return sorted(self.values)[0]

    @property
    def high(self):
        if self.values and len(self.values) == 2:
            return sorted(self.values)[1]

    def is_ready(self):
        return len(self.values) == 2

    def reset(self):
        self.values = []


def parse():
    inputs = []
    instructions = []
    bot_by_id = {}
    output_by_id = {}
    ids = set()
    outputs = set()

    for line in fileinput.input():
        words = line.strip().split()
        if line.startswith("value"):
            # "value 43 goes to bot 90"
            value = int(words[1])
            bot = int(words[-1])
            ids.add(bot)
            inputs.append((value, bot))
        else:
            # "bot 75 gives low to bot 7 and high to bot 113"
            bot = int(words[1])
            low_to_type = words[5]
            low_to_id = int(words[6])
            high_to_type = words[-2]
            high_to_id = int(words[-1])
            ids.add(bot)
            if low_to_type == "bot":
                ids.add(low_to_id)
            else:
                outputs.add(low_to_id)
            if high_to_type == "bot":
                ids.add(high_to_id)
            else:
                outputs.add(high_to_id)

            instructions.append((bot, low_to_type, low_to_id, high_to_type, high_to_id))

    for id in ids:
        bot_by_id[id] = Bot(id)

    for id in outputs:
        output_by_id[id] = None

    return inputs, instructions, bot_by_id, output_by_id


def run(
    bot_by_id: Dict[int, Bot],
    output_by_id: Dict[int, int],
    inputs: List[Tuple[int, int]],
    instructions: List[Tuple[int, str, int, str, int]],
    compare: Tuple[int, int],
):
    for value, bot in inputs:
        bot_by_id[bot].values.append(value)

    while any(output is None for output in output_by_id.values()):
        for bot, low_to_type, low_to_id, high_to_type, high_to_id in instructions:
            if bot_by_id[bot].is_ready():
                low = bot_by_id[bot].low
                high = bot_by_id[bot].high

                if sorted([low, high]) == sorted(compare):
                    print(f"Part 1: bot {bot} compared {compare}")

                if low_to_type == "bot":
                    bot_by_id[low_to_id].values.append(low)
                else:
                    output_by_id[low_to_id] = low

                if high_to_type == "bot":
                    bot_by_id[high_to_id].values.append(high)
                else:
                    output_by_id[high_to_id] = high

                bot_by_id[bot].reset()
    return output_by_id


def main():
    inputs, instructions, bot_by_id, output_by_id = parse()
    run(bot_by_id, output_by_id, inputs, instructions, compare=(17, 61))
    print(f"Part 2: {prod([output_by_id[id] for id in [0, 1, 2]])}")


if __name__ == "__main__":
    main()
