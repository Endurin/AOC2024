from pathlib import Path


filedir = Path(__file__).parent.resolve()
VERIFICATION = filedir.joinpath("inputs/verification.txt")
INPUT = filedir.joinpath("inputs/input.txt")

def read_input(path: Path) -> tuple[list, list]:
    pieces = []
    targets = []
    first_line = True
    for line in open(path, 'r'):
        line = line.strip()
        if first_line:
            first_line = False
            for num in line.split(','):
                pieces.append(num.strip())
        else:
            if not len(line):
                continue
            targets.append(line)

    return pieces, targets


def count_combinations(target: str, pieces: list[str], solved: dict) -> int:
    if target == '':
        return 1
    
    if target in solved:
        return solved[target]

    # brute force combinations by stripping off the first part
    total = 0
    for piece in pieces:
        if target.startswith(piece):
            total += count_combinations(target[len(piece):], pieces, solved)
    # and store all the solutions found
    solved[target] = total
    return total
   

def part2(path: Path) -> int:
    pieces, targets = read_input(path)
    solved = dict() # keep track of already solved sub-pieces to avoid double work
    possibilities = 0
    for t in targets:
        possibilities += count_combinations(t, pieces, solved)

    return possibilities

assert(count_combinations('a',['a'],dict())==1)
assert(count_combinations('ab',['a','b'],dict())==1)
assert(count_combinations('acb',['a','b','c'],dict())==1)
assert(count_combinations('abc',['a','bc'],dict())==1)
assert(count_combinations('br',['br','b','r'],dict())==2)
assert(count_combinations('bggr',['r','g','b'],dict())==1)
assert(count_combinations('brwrr',['wr','br','a','b','r'],dict())==2)
assert(part2(VERIFICATION) == 16)
print(part2(INPUT))
