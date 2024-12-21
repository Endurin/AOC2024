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

def try_solve(target: str, pieces: list[str], solved: set, failures: set) -> bool:
    if target in solved:
        return True
    if target in failures:
        return False

    for piece in pieces:
        success = False
        if piece in target:
            sub_targets = target.split(piece)
            for s in sub_targets:
                success = True
                if s in solved:
                    continue
                if not try_solve(s, pieces, solved, failures):
                    failures.add(s)
                    success = False
                    break
        
            if success:
                solved.add(target)
                return True
    
    return False
    

def part1(path: Path) -> int:
    pieces, targets = read_input(path)
    pieces.sort(key=len, reverse=True) # sort long->short
    solved = set(pieces) # keep track of already solved sub-pieces to avoid double work
    solved.add('')
    failures = set() # keep track of already failed sub-pieces to avoid double work
    num_solved = 0
    for t in targets:
        num_solved += try_solve(t, pieces, solved, failures)

    return num_solved


assert(part1(VERIFICATION) == 6)
print(part1(INPUT))
