def read_map(filename):
    with open(filename, "r") as r:
        return [line.strip() for line in r]
    