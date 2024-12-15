from pathlib import Path
import regex as re


filedir = Path(__file__).parent.resolve()
VERIFICATION = filedir.joinpath("inputs/verification.txt")
INPUT = filedir.joinpath("inputs/input.txt")

def read_input(path: Path):
    button_as = []
    button_bs = []
    prizes = []
    for line in open(path, 'r'):
        line = line.strip()
        if line.startswith('Button A'):
            match = re.findall(r'(\d+)', line)
            button_as.append((int(match[0]), int(match[1])))
        elif line.startswith('Button B'):
            match = re.findall(r'(\d+)', line)
            button_bs.append((int(match[0]), int(match[1])))
        elif line.startswith('Prize'):
            match = re.findall(r'(\d+)', line)
            prizes.append((int(match[0]), int(match[1])))

    return button_as, button_bs, prizes

def cost_to_win_prize(a,b,p) -> int:
    for i in range(101):
        ax = a[0]*i
        ay = a[1]*i
        for j in range(101):
            x = ax + b[0]*j
            y = ay + b[1]*j
            if x == p[0] and y == p[1]: #success!
                return 3*i + j
            if x > p[0] or y > p[1]: #failure!
                break
    return 0

def solve_brute_force(path: Path) -> int:
    button_as, button_bs, prizes = read_input(path)
    cost = 0
    for (a,b,p) in zip(button_as,button_bs,prizes):
        cost += cost_to_win_prize(a,b,p)

    return cost

def cost_analytical(a, b, p, add_to_prize) -> int:
    i = ((p[0]+add_to_prize)*b[1]-(p[1]+add_to_prize)*b[0]) / (a[0]*b[1] - a[1]*b[0])
    j = ((p[0]+add_to_prize) - a[0]*i) / b[0]
    # If the analytical result gives an integer, we have a winner
    if int(i) == i and int(j) == j:
        return int(i*3 + j)
    return 0

def solve_analytical(path: Path, add_to_prize = 0) -> int:
    button_as, button_bs, prizes = read_input(path)
    cost = 0
    for (a,b,p) in zip(button_as,button_bs,prizes):
        cost += cost_analytical(a,b,p, add_to_prize)

    return cost

assert(solve_brute_force(VERIFICATION) == 480)
print(solve_brute_force(INPUT))
assert(solve_analytical(VERIFICATION) == 480)
print(solve_analytical(INPUT, add_to_prize=10000000000000))
