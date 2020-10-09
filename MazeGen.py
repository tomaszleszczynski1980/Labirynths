import random


class Room:
    """Room in the maze that is surrounded by walls - north, east, south, west."""

    # A wall separates a pair of rooms in the N-S or W-E directions.
    wall_pairs = {'N': 'S', 'S': 'N', 'E': 'W', 'W': 'E'}

    def __init__(self, x, y):
        """Initialize room with all four walls"""

        self.x = x
        self.y = y
        self.walls = {'N': True, 'S': True, 'E': True, 'W': True}

    def has_all_walls(self) -> bool:
        """Does this room have all walls?"""

        return all(self.walls.values())

    def destroy_wall(self, other, wall):
        """Destroy the wall between rooms self and other."""

        self.walls[wall] = False
        other.walls[Room.wall_pairs[wall]] = False


class Maze:
    """Maze represented as a grid of cells."""

    def __init__(self, width, height, start_x=0, start_y=0):
        """Initialize maze grid.
        The maze consists of nx * ny cells
        and will be constructed starting at the cell indexed (ix, iy).
        """

        self.width = width
        self.height = height
        self.start_x = start_x
        self.start_y = start_y
        self.maze_map = [[Room(x, y) for y in range(height)] for x in range(width)]

    def room_at(self, x, y) -> Room:
        """Return Room object at (x, y)."""

        return self.maze_map[x][y]

    def __str__(self) -> str:
        """Return the maze as a string"""

        maze_rows = ['-' * self.width * 2]
        for y in range(self.height):
            maze_row = ['|']
            for x in range(self.width):
                if self.maze_map[x][y].walls['E']:
                    maze_row.append(' |')
                else:
                    maze_row.append('  ')
            maze_rows.append(''.join(maze_row))
            maze_row = ['|']
            for x in range(self.width):
                if self.maze_map[x][y].walls['S']:
                    maze_row.append('-+')
                else:
                    maze_row.append(' +')
            maze_rows.append(''.join(maze_row))

        return '\n'.join(maze_rows)

    def find_valid_neighbours(self, room) -> list:
        """Return a list of unvisited neighbours of room."""

        directions = [('W', (-1, 0)), ('E', (1, 0)), ('S', (0, 1)), ('N', (0, -1))]
        neighbours = []
        for direction, (dx, dy) in directions:
            x2 = room.x + dx
            y2 = room.y + dy

            if (0 <= x2 < self.width) and (0 <= y2 < self.height):
                neighbour = self.room_at(x2, y2)
                if neighbour.has_all_walls():
                    neighbours.append((direction, neighbour))

        return neighbours

    def make_maze(self):
        """Builds maze."""

        total_rooms = self.width * self.height
        total_visited_rooms = 1
        rooms_stack = []
        current_room = self.room_at(self.start_x, self.start_y)

        while total_visited_rooms < total_rooms:
            neighbours = self.find_valid_neighbours(current_room)

            if not neighbours:
                # Moving back
                current_room = rooms_stack.pop()
                continue

            # Choose a random neighbouring room and go there.
            direction, next_room = random.choice(neighbours)
            current_room.destroy_wall(next_room, direction)
            rooms_stack.append(current_room)
            current_room = next_room
            total_visited_rooms += 1

    def write_txt(self, filename):
        """Write maze as a string to txt file."""

        with open(filename, 'w') as file:
            print(self, file=file)

    def write_svg(self, filename):
        """Write maze as an SVG image to file."""

        aspect_ratio = self.width / self.height
        # Pad the maze all around by this amount.
        padding = 10
        # Height and width of the maze image (excluding padding), in pixels
        height = 500
        width = int(height * aspect_ratio)
        # Scaling factors mapping maze coordinates to image coordinates
        scy = height / self.height
        scx = width / self.width

        def write_wall(file, x1, y1, x2, y2):
            """Write a single wall to the SVG image file."""

            print(f'<line x1="{x1}" y1="{y1}" x2="{x2}" y2="{y2}"/>', file=file)

        # Write the SVG image file for maze
        with open(filename, 'w') as file:
            # SVG header and styles.
            print('<?xml version="1.0" encoding="utf-8"?>', file=file)
            print('<svg xmlns="http://www.w3.org/2000/svg"', file=file)
            print('    xmlns:xlink="http://www.w3.org/1999/xlink"', file=file)
            print('    width="{:d}" height="{:d}" viewBox="{} {} {} {}">'
                  .format(width + 2 * padding, height + 2 * padding, -padding, -padding, width + 2 * padding,
                          height + 2 * padding),
                  file=file)
            print('<defs>\n<style type="text/css"><![CDATA[', file=file)
            print('line {', file=file)
            print('    stroke: #000000;\n    stroke-linecap: square;', file=file)
            print('    stroke-width: 5;\n}', file=file)
            print(']]></style>\n</defs>', file=file)
            # Draw the "South" and "East" walls of each room if present
            # (these are the "North" and "West" walls of a neighbouring room).
            for x in range(self.width):
                for y in range(self.height):
                    if self.room_at(x, y).walls['S']:
                        x1, y1, x2, y2 = x * scx, (y + 1) * scy, (x + 1) * scx, (y + 1) * scy
                        write_wall(file, x1, y1, x2, y2)
                    if self.room_at(x, y).walls['E']:
                        x1, y1, x2, y2 = (x + 1) * scx, y * scy, (x + 1) * scx, (y + 1) * scy
                        write_wall(file, x1, y1, x2, y2)
            # Draw the North and West maze border, which won't have been drawn above.
            print(f'<line x1="0" y1="0" x2="{width}" y2="0"/>', file=file)
            print(f'<line x1="0" y1="0" x2="0" y2="{height}"/>', file=file)
            print('</svg>', file=file)


def main():
    filename = input('filename >>>')
    nx = int(input('maze dimension x>>>'))
    ny = int(input('maze dimension y>>>'))
    ix = int(input('entry point x>>>'))
    iy = int(input('entry point y>>>'))

    maze = Maze(nx, ny, ix, iy)
    maze.make_maze()

    maze.write_svg(filename + '.svg')
    maze.write_txt(filename + '.txt')
    print(maze)


if __name__ == "__main__":
    main()
