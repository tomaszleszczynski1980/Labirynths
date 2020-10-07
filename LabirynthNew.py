import heapq
from sys import argv


def parse_map(mapa, origin=None, destination=None):

    lines = mapa.splitlines()

    if not origin:
        origin = (0, 0)
    if not destination:
        destination = (len(lines[-1]) - 1, len(lines) - 1)

    return lines, origin, destination


def is_valid(lines, position, passables=". "):

    x, y = position
    if not (0 <= y < len(lines) and 0 <= x < len(lines[y])):
        return False

    if lines[y][x] in passables:
        return True

    return False


def get_neighbours(lines, current):

    x, y = current
    for dx in [-1, 0, 1]:
        for dy in [-1, 0, 1]:
            if dx == 0 and dy == 0:
                continue

            position = x + dx, y + dy
            if is_valid(lines, position):

                yield position


def get_shorter_paths(tentative, positions, through):

    path = tentative[through] + [through]
    for position in positions:
        if position in tentative and len(tentative[position]) <= len(path):
            continue

        yield position, path


def find_path(mapa):

    lines, origin, destination = parse_map(mapa)
    tentative = {origin: []}
    candidates = [(0, origin)]
    certain = set()

    while destination not in certain and len(candidates) > 0:
        _ignored, current = heapq.heappop(candidates)

        if current in certain:
            continue

        certain.add(current)
        neighbours = set(get_neighbours(lines, current)) - certain

        shorter = get_shorter_paths(tentative, neighbours, current)

        for neighbour, path in shorter:
            tentative[neighbour] = path
            heapq.heappush(candidates, (len(path), neighbour))

    if destination in tentative:
        return tentative[destination] + [destination]
    else:
        raise ValueError("no path")


def show_path(path, mapa):

    lines = mapa.splitlines()
    for x, y in path:
        lines[y] = lines[y][:x] + "@" + lines[y][x + 1:]

    return "\n".join(lines) + "\n"


def main(filename):

    try:
        with open(filename, mode='r') as file:
            map = file.read()
            path = find_path(map)
            print(show_path(path, map))

    except FileNotFoundError:
        print(f'File {filename} not found')

    except ValueError as error:
        print(error)


if __name__ == "__main__":

    if len(argv) > 1:
        filename = argv[1]
    else:
        filename = input('Map file name>>> ')

    main(filename)
