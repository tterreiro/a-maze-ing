from typing import Any


def parse_map(filename: str) -> dict[str, Any]:
    """Parse configuration file and validate maze settings."""
    config = {}
    with open(filename, "r") as f:
        for line in f:
            line = line.strip()
            if line.startswith('#'):
                continue
            if not line or '=' not in line:
                raise ValueError("Every line should be 'KEY=VALUE'")
            value: Any
            key, value = line.split('=', 1)
            key = key.strip().upper()
            value = value.strip()
            # cast for data type correct
            if key in ('WIDTH', 'HEIGHT'):
                value = int(value)
            elif key in ('ENTRY', 'EXIT'):
                x_str, y_str = value.split(',')
                value = (int(x_str), int(y_str))
            elif key == 'PERFECT':
                if value.lower() not in ('true', 'false'):
                    raise ValueError("PERFECT must be true or false")
                value = value.lower() == 'true'
            elif key == 'SEED':
                try:
                    value = int(value)
                except Exception:
                    value = None
            config[key] = value

    # config map validations
    required_keys = [
        'WIDTH', 'HEIGHT', 'ENTRY', 'EXIT', 'OUTPUT_FILE', 'PERFECT'
        ]
    for k in required_keys:
        if k not in config:
            raise ValueError(f"Missing key in config: {k}")
    # aditional validations
    entry = config['ENTRY']
    exit = config['EXIT']
    width = config['WIDTH']
    height = config['HEIGHT']

    if width < 2:
        raise ValueError("Width too low!")
    if height < 2:
        raise ValueError("Height too low")
    # ENTRY and EXIT can not be equal
    if entry == exit:
        raise ValueError("Entry value cant be equal to EXIT ")
    if (width < 10 and height < 10):
        print("Maze too small for 42 logo!")
    if (width > 10 and height > 10):
        if (((width//2-3) <= entry[0] <= (width//2+3))
                and ((height//2-2) <= entry[1] <= (height//2+2))):
            raise ValueError("Entry cant be in the middle of the maze!")
        if (((width//2-3) <= exit[0] <= (width//2+3))
                and ((height//2-2) <= exit[1] <= (height//2+2))):
            raise ValueError("Exit cant be in the middle of the maze!")
    else:
        print("Maze too small for 42 logo")
    # no value can be negative or out of map
    if entry[0] < 0 or entry[1] < 0 or exit[0] < 0 or exit[1] < 0:
        raise ValueError("Coordenates can't be negative")
    if (entry[0] >= width or entry[1] >= height
            or exit[0] >= width or exit[1] >= height):
        raise ValueError("ENTRY or EXIT can't be outside the maze")
    return config
