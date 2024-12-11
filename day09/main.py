from pathlib import Path

filedir = Path(__file__).parent.resolve()
VERIFICATION = filedir.joinpath("inputs/verification.txt")
INPUT = filedir.joinpath("inputs/input.txt")

def read_input(path: Path) -> ...:
    rv = []
    for line in open(path, 'r'):
        line = line.strip()
        for char in line:
            rv.append(int(char))
    return rv

def expand_to_data(compressed_format: list) -> list:
    expanded = []
    data = True
    data_index = 0
    for blocksize in compressed_format:
        expanded.extend([data_index if data else -1]*blocksize)
        if data:
            data_index += 1
        data = not data
    return expanded

def compress(data: list):
    iter_front = 0
    iter_back = len(data) - 1
    while iter_back > iter_front:
        if data[iter_front] != -1:
            iter_front += 1
            continue
        if data[iter_back] == -1: # can this happen?
            iter_back -= 1
            continue
        data[iter_front], data[iter_back] = data[iter_back], data[iter_front]
        iter_front += 1
        iter_back -= 1

def get_checksum(compressed_data: list) -> int:
    sum = 0
    for i, a in enumerate(compressed_data):
        if a == -1:
            continue
        sum += i * a
    return sum

def part1(path: Path) -> int:
    inputs = read_input(path)
    data = expand_to_data(inputs)
    compress(data)
    checksum = get_checksum(data)

    return checksum

def try_fit(data, iter_back, block_size):
    iter_front = 0
    while iter_front < iter_back:
        # grab first -1
        if data[iter_front] != -1:
            iter_front += 1
            continue
        
        # find size of space
        space_size = 1
        while data[iter_front + space_size] == -1:
            space_size += 1

        # swap if found
        if space_size >= block_size:
            for i in range(block_size):
                data[iter_front+i], data[iter_back+i] = data[iter_back+i], data[iter_front+i]
            return
        
        iter_front += 1


def compress_contiguous(data: list):
    iter_back = len(data) - 1
    while iter_back > 0:
        if data[iter_back] == -1:
            iter_back -= 1
            continue

        # find start and size of block
        block_size = 1
        while data[iter_back - 1] == data[iter_back]:
            iter_back -= 1
            block_size += 1

        # loop from front, try to fit
        try_fit(data, iter_back, block_size)
        iter_back -= 1

def get_last(a):
  for i, e in enumerate(reversed(a)):
    if e is not -1:
      return len(a) - i - 1
  return -1

def part2(path: Path) -> int:
    inputs = read_input(path)

    data = expand_to_data(inputs)
    compress_contiguous(data)
    last_idx = get_last(data)

    checksum = get_checksum(data)

    return checksum



assert(part1(VERIFICATION) == 1928)
print(part1(INPUT))
assert(part2(VERIFICATION) == 2858)
print(part2(INPUT))
