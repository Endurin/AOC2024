from pathlib import Path
import regex as re
import os

filedir = Path(__file__).parent.resolve()
VERIFICATION = filedir.joinpath("inputs/verification.txt")
VERIFICATION2 = filedir.joinpath("inputs/verification2.txt")
INPUT = filedir.joinpath("inputs/input.txt")

def part1(path: Path) -> int:
    sum = 0
    for line in open(path, 'r'):
        for match in re.findall(r'mul\((\d+),(\d+)\)', line):
            sum += int(match[0]) * int(match[1])
    return sum

def part2(path: Path) -> int:
    sum = 0
    first = True
    for line in open(path, 'r'):
        # Anything following a don't() is invalid
        sections = line.split('don\'t()')
        allowed_sections = []
        for section in sections:
            allowed_section = section.split('do()')
            # Until we find a do() or we're at the very start
            if(first):
                allowed_sections.extend(allowed_section[0:1])
                first = False
            allowed_sections.extend(allowed_section[1:])

        for s in allowed_sections:
            for match in re.findall(r'mul\((\d+),(\d+)\)', s):
                sum += int(match[0]) * int(match[1])

    return sum


assert(part1(VERIFICATION) == 161)
print(part1(INPUT))
assert(part2(VERIFICATION2) == 48)
print(part2(INPUT))
