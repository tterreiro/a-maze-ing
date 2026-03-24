def read_map(filename):
    with open(filename, "r") as r:
        return [line.strip() for line in r]

def parse_map(lines):
    return [list(line) for line in lines]