from time import perf_counter
import queue


class Maze:
    def __init__(self, list_view: list[list[str]]) -> None:
        self.list_view = list_view
        self.start_j = None
        for j, sym in enumerate(self.list_view[0]):
            if sym == "O":
                self.start_j = j

    @classmethod
    def from_file(cls, filename):
        list_view = []
        with open(filename, "r") as f:
            for l in f.readlines():
                list_view.append(list(l.strip()))
        obj = cls(list_view)
        return obj

    def print(self, path="") -> None:
        # Find the path coordinates
        i = 0  # in the (i, j) pair, i is usually reserved for rows and j is reserved for columns
        j = self.start_j
        path_coords = set()
        for move in path:
            i, j = _shift_coordinate(i, j, move)
            path_coords.add((i, j))
        # Print maze + path
        for i, row in enumerate(self.list_view):
            for j, sym in enumerate(row):
                if (i, j) in path_coords:
                    print("+ ", end="")  # NOTE: end is used to avoid linebreaking
                else:
                    print(f"{sym} ", end="")
            print()  # linebreak


def solve(maze: Maze) -> None:
    path = ""  # solution as a string made of "L", "R", "U", "D"

    cord_i_j = (0, maze.start_j)

    q = queue.Queue()
    visited = set()

    q.put((path, cord_i_j))
    visited.add(cord_i_j)

    while not q.empty():
        (t_path, t_cord_i_j) = q.get()

        if maze.list_view[t_cord_i_j[0]][t_cord_i_j[1]] == "X":
            path = t_path
            break
        else:
            for i in ("L", "R", "U", "D"):
                a = _shift_coordinate(t_cord_i_j[0], t_cord_i_j[1], i)
                if (0 <= a[0] <= len(maze.list_view)) and (0 <= a[1] <= len(maze.list_view[a[0]])):
                    if maze.list_view[a[0]][a[1]] != "#" and a not in visited:
                        q.put((t_path+i, a))
                        visited.add(a)



    print(f"Found: {path}")
    maze.print(path)


def _shift_coordinate(i: int, j: int, move: str) -> tuple[int, int]:
    if move == "L":
        j -= 1
    elif move == "R":
        j += 1
    elif move == "U":
        i -= 1
    elif move == "D":
        i += 1
    return (i, j)


if __name__ == "__main__":
    maze = Maze.from_file("maze_3.txt")
    t_start = perf_counter()
    solve(maze)
    t_end = perf_counter()
    print(f"Elapsed time: {t_end - t_start} sec")
