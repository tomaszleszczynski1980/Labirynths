import heapq

class PathFinder:

    def __init__(self, mapa, passables=' ', origin=None, destination=None):
        self.mapa = mapa
        self.passables = passables
        self.origin = origin
        self.destination = destination

    def parse_map(self):
        lines = self.mapa.splitlines()

        if not self.origin:
            self.origin = (1, 1)
        if not self.destination:
            self.destination = (len(lines[-1]) - 2, len(lines) - 2)

        return lines

    def is_valid(self, lines, position):

        x, y = position
        if not (0 <= y < len(lines) and 0 <= x < len(lines[y])):
            return False

        if lines[y][x] in self.passables:
            return True

        return False

    def get_neighbours(self, lines, current):

        x, y = current
        for dx in [-1, 0, 1]:
            for dy in [-1, 0, 1]:
                if dx == 0 and dy == 0:
                    continue

                position = x + dx, y + dy
                if self.is_valid(lines, position):

                    yield position

    def get_shorter_paths(self, tentative, positions, through):

        path = tentative[through] + [through]
        for position in positions:
            if position in tentative and len(tentative[position]) <= len(path):
                continue

            yield position, path

    def find_path(self):

        lines = self.parse_map()
        tentative = {self.origin: []}
        candidates = [(0, self.origin)]
        certain = set()

        while self.destination not in certain and len(candidates) > 0:
            _ignored, current = heapq.heappop(candidates)

            if current in certain:
                continue

            certain.add(current)
            neighbours = set(self.get_neighbours(lines, current)) - certain

            shorter = self.get_shorter_paths(tentative, neighbours, current)

            for neighbour, path in shorter:
                tentative[neighbour] = path
                heapq.heappush(candidates, (len(path), neighbour))

        if self.destination in tentative:
            return tentative[self.destination] + [self.destination]
        else:
            raise ValueError("no path")

    def __str__(self, path_symbol="@"):

        path = self.find_path()
        lines = self.mapa.splitlines()
        for x, y in path:
            lines[y] = lines[y][:x] + path_symbol + lines[y][x + 1:]

        return "\n".join(lines) + "\n"

