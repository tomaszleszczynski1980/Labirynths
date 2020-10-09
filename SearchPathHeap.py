import heapq


class PathFinder:

    def __init__(self, mapa, passables=' ', origin=None, destination=None):
        self.mapa = mapa
        self.passables = passables
        self.origin = origin
        self.destination = destination
        self.lines = list()

    def parse_map(self):
        self.lines = self.mapa.splitlines()
        if not self.origin:
            self.origin = (1, 1)
        if not self.destination:
            self.destination = (len(self.lines[-1]) - 2, len(self.lines) - 2)

        return self.lines

    def is_valid(self, position):
        x, y = position
        if not (0 <= y < len(self.lines) and 0 <= x < len(self.lines[y])):
            return False

        if self.lines[y][x] in self.passables:
            return True

        return False

    def get_neighbours(self, current):
        x, y = current
        for direction_x in [-1, 0, 1]:
            for direction_y in [-1, 0, 1]:
                if direction_x == 0 and direction_y == 0:
                    continue

                position = x + direction_x, y + direction_y
                if self.is_valid(position):
                    yield position

    def get_shorter_paths(self, test_paths: dict, positions, through):
        """Paths to selected positions generator"""
        path = test_paths[through] + [through]
        for position in positions:
            if position in test_paths and len(test_paths[position]) <= len(path):
                continue

            yield position, path

    def find_path(self):
        test_paths = {self.origin: []}  # map(dictionary) of a tentative path from the origin to a position
        candidates = [(0, self.origin)]    # heap of positions that have paths to destination, sorting key = len(path)
        certain = set()  # set of points for which the path in test_paths is certain to be the shortest possible path.

        while self.destination not in certain and len(candidates) > 0:
            _ignore_it, current = heapq.heappop(candidates)

            if current in certain:
                continue

            certain.add(current)
            neighbours = set(self.get_neighbours(current)) - certain

            shorter = self.get_shorter_paths(test_paths, neighbours, current)

            for neighbour, path in shorter:
                test_paths[neighbour] = path
                heapq.heappush(candidates, (len(path), neighbour))

        if self.destination in test_paths:
            return test_paths[self.destination] + [self.destination]
        else:
            raise ValueError("no path")

    def __str__(self, path_symbol="@"):
        path = self.find_path()
        lines = self.mapa.splitlines()
        for x, y in path:
            lines[y] = lines[y][:x] + path_symbol + lines[y][x + 1:]

        return "\n".join(lines) + "\n"
