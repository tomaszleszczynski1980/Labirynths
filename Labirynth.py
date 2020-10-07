labirynth = [[1, 0, 1, 1, 1],
             [1, 0, 1, 0, 1],
             [1, 0, 0, 0, 1],
             [1, 0, 1, 0, 1],
             [1, 0, 0, 0, 1],
             [1, 0, 1, 0, 1],
             [1, 0, 1, 0, 1]]

path = []


def LabirynthSearch(labirynth: list, start: tuple, end: tuple):

    print(path)

    MOVES = ((-1, 0), (0, 1), (1, 0), (0, -1))

    if start == end:
        print("finished")
        return True

    else:
        labirynth[start[0]][start[1]] = 1
        path.append(start)

        for move in MOVES:
            next_row = start[0] + move[0]
            next_col = start[1] + move[1]

            if (0 <= next_col < len(labirynth[0])) and (0 <= next_row < len(labirynth)):

                if labirynth[next_row][next_col] == 0:
                    LabirynthSearch(labirynth, (next_row, next_col), end)

        previous = path.pop()
        labirynth[previous[0]][previous[1]] = 0
        return False


done = LabirynthSearch(labirynth, (0, 1), (6, 3))

# there is problem with final path and final done
# print(path)
# print(done)
