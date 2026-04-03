from typing import Any


def read_map(filename: str) -> list[str]:
    with open(filename, "r") as r:
        return [line.strip() for line in r]


def parse_map(filename: str) -> dict:
    config = {}
    with open(filename, "r") as f:
        for line in f:
            line = line.strip()
            if not line or '=' not in line:
                continue
            value: Any
            key, value = line.split('=', 1)
            key = key.strip().upper()
            value = value.strip()
            # cast para o data type correto
            if key in ('WIDTH', 'HEIGHT'):
                value = int(value)
            elif key in ('ENTRY', 'EXIT'):
                x_str, y_str = value.split(',')
                value = (int(x_str), int(y_str))
            elif key == 'PERFECT':
                value = value.lower() == 'true'
            config[key] = value

    # validações da config do mapa
    required_keys = [
        'WIDTH', 'HEIGHT', 'ENTRY', 'EXIT', 'OUTPUT_FILE', 'PERFECT'
        ]
    for k in required_keys:
        if k not in config:
            raise ValueError(f"Missing key in config: {k}")
    # validações adicionais
    entry = config['ENTRY']
    exit = config['EXIT']
    width = config['WIDTH']
    height = config['HEIGHT']

    # ENTRY e EXIT não podem ser iguais
    if entry == exit:
        raise ValueError("Entry value cant be equal to EXIT ")
    # nenhum valor pode ser negativo ou fora do mapa
    if entry[0] < 0 or entry[1] < 0 or exit[0] < 0 or exit[1] < 0:
        raise ValueError("Coordenadas não podem ser negativas")
    if (entry[0] >= width or entry[1] >= height
            or exit[0] >= width or exit[1] >= height):
        raise ValueError("Coordenadas ENTRY ou EXIT fora do mapa")
    return config
