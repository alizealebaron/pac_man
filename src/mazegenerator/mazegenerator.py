import random
from collections import deque
from typing import Iterator


class MazeGenerator:

    def __init__(self, size: tuple[int, int] = (15, 15), perfect: bool = False,
                 entry_cell: tuple[int, int] = (0, 0),
                 exit_cell: tuple[int, int] = (-1, -1),
                 seed: int = 0) -> None:
        self._width = size[0]
        self._height = size[1]
        self._perfect = perfect
        self._seed = seed
        self._entryx = (entry_cell[0]
                        if 0 <= entry_cell[0] < self._width else 0)
        self._entryy = (entry_cell[1]
                        if 0 <= entry_cell[1] < self._height else 0)
        self._exitx = (exit_cell[0]
                       if 0 <= exit_cell[0] < self._width else self._width-1)
        self._exity = (exit_cell[1]
                       if 0 <= exit_cell[1] < self._height else self._height-1)
        self._maze: list[list[int]] = []
        self._path: list[list[int]] = []
        self._shortest_path: str | bool = False
        self.generate(self._seed)
        return None

    @property
    def maze(self) -> list[list[int]]:
        return self._maze

    @property
    def shortest_path(self) -> str | bool:
        return self._shortest_path

    @property
    def maze_entry(self) -> tuple[int, int]:
        return self._entryx, self._entryy

    @property
    def maze_exit(self) -> tuple[int, int]:
        return self._exitx, self._exity

    def generate(self, seed: int = 0) -> None:
        random.seed(seed) if seed > 0 else random.seed()
        self._seed = seed
        self._create_empty_maze()
        self._add_42_to_maze()
        self._generate_maze(self._entryx, self._entryy, 0)
        if self._perfect is False:
            self._braid()
        self._find_short_path()

#    Private functions

    def _braid(self) -> None:
        # Pac-Man-compatible maze: remove every dead-end (a corridor with a
        # single opening) by carving one extra passage, so a chased player is
        # never trapped. The isolated '42' cells (value 15) and the outer
        # border are left untouched. Opening a wall only raises both cells'
        # degree, so a single pass cannot create a new dead-end.
        directions = [(0, -1, 1, 4), (1, 0, 2, 8),
                      (0, 1, 4, 1), (-1, 0, 8, 2)]   # dx, dy, code, opp_code
        for y in range(self._height):
            for x in range(self._width):
                if self._maze[y][x] == 15:           # isolated '42' cell
                    continue
                while bin(self._maze[y][x] & 0xF).count('1') >= 3:
                    options = []
                    for dx, dy, code, opp in directions:
                        nx, ny = x + dx, y + dy
                        if (0 <= nx < self._width and 0 <= ny < self._height
                                and (self._maze[y][x] & code)
                                and self._maze[ny][nx] != 15):
                            options.append((nx, ny, code, opp))
                    if not options:
                        break
                    nx, ny, code, opp = random.choice(options)
                    self._maze[y][x] &= ~code
                    self._maze[ny][nx] &= ~opp

    def _create_empty_maze(self) -> None:
        self._maze = [[8] + [0] * (self._width-2) +
                      [2] for _ in range(self._height-2)]
        self._maze.insert(0, [9] + [1] * (self._width-2) + [3])
        self._maze.append([12] + [4] * (self._width-2) + [6])
        self._path = [[0] * self._width for _ in range(self._height)]

    def _add_42_to_maze(self) -> None:
        ft_small = [[1, 0, 0, 0, 1, 1, 1],
                    [1, 0, 0, 0, 0, 0, 1],
                    [1, 1, 1, 0, 1, 1, 1],
                    [0, 0, 1, 0, 1, 0, 0],
                    [0, 0, 1, 0, 1, 1, 1]
                    ]
        if len(ft_small)*2 > self._height or len(ft_small[0])*2 > self._width:
            print("MazeGenerator Warning: maze is too small to add '42' in it")
            return
        posy = int((self._height - len(ft_small)) / 2)
        posx = int((self._width - len(ft_small[0])) / 2)
        for y in range(len(ft_small)):
            for x in range(len(ft_small[0])):
                if ft_small[y][x] == 1:
                    self._maze[posy+y][posx+x] = 15
                    self._maze[posy+y][posx+x-1] |= 2
                    self._maze[posy+y][posx+x+1] |= 8
                    self._maze[posy+y-1][posx+x] |= 4
                    self._maze[posy+y+1][posx+x] |= 1
                    self._path[posy+y][posx+x] = 1

    def _is_available(self, x: int, y: int) -> bool:
        if (
                0 <= y < self._height and
                0 <= x < self._width and self._path[y][x] == 0
        ):
            return True
        return False

    def _get_neighbors(self, x: int,
                       y: int) -> Iterator[tuple[int, int, int, int]]:
        directions = [(1, 0, 2, 8), (-1, 0, 8, 2), (0, 1, 4, 1), (0, -1, 1, 4)]
        random.shuffle(directions)
        for dw, dh, code, opp_code in directions:
            nx, ny = x + dw, y + dh
            if self._is_available(nx, ny):
                yield nx, ny, code, opp_code
            else:
                if (
                        self._perfect is False and random.randint(0, 5) == 0
                        and 0 <= ny < self._height and 0 <= nx < self._width
                ):
                    if (
                            self._maze[ny][nx] != 15 and
                            (self._maze[y][x] & (~code)) != 0 and
                            (self._maze[ny][nx] & (~opp_code)) != 0
                    ):
                        self._maze[y][x] = self._maze[y][x] & (~code)
                        self._maze[ny][nx] = self._maze[ny][nx] & (~opp_code)

    def _generate_maze(self, x: int, y: int, from_code: int) -> None:
        # Iterative depth-first carving with an explicit stack, so very large
        # mazes never hit Python's recursion limit. Each frame keeps its own
        # neighbour generator, which preserves the original lazy evaluation
        # order (and its random side effects) exactly as the recursive version.
        def _enter(cx, cy, fcode):
            self._path[cy][cx] = 1
            non_mutable = self._maze[cy][cx]
            self._maze[cy][cx] = 15 & ~fcode
            return [cx, cy, non_mutable, self._get_neighbors(cx, cy)]

        stack = [_enter(x, y, from_code)]
        while stack:
            cx, cy, non_mutable, gen = stack[-1]
            advanced = False
            for nx, ny, code, opp_code in gen:
                if code & non_mutable:
                    continue
                self._maze[cy][cx] = self._maze[cy][cx] & (~code)
                stack.append(_enter(nx, ny, opp_code))
                advanced = True
                break
            if not advanced:
                stack.pop()

    def _find_short_path(self) -> None:
        # BFS: shortest entry->exit path in O(cells). Robust on looped (braided)
        # mazes, where the previous depth-first search exploded exponentially.
        moves = [(0, -1, 1, 'N'), (1, 0, 2, 'E'),
                 (0, 1, 4, 'S'), (-1, 0, 8, 'W')]   # dx, dy, wall code, letter
        start = (self._entryx, self._entryy)
        goal = (self._exitx, self._exity)
        prev: dict = {start: None}
        queue = deque([start])
        while queue:
            x, y = queue.popleft()
            if (x, y) == goal:
                break
            for dx, dy, code, letter in moves:
                nx, ny = x + dx, y + dy
                if (0 <= nx < self._width and 0 <= ny < self._height
                        and (self._maze[y][x] & code) == 0
                        and (nx, ny) not in prev):
                    prev[(nx, ny)] = ((x, y), letter)
                    queue.append((nx, ny))
        if goal not in prev:
            self._shortest_path = False
            print("MazeGenerator Class error: no shortest path found.")
            return
        letters = []
        cur = goal
        while prev[cur] is not None:
            parent, letter = prev[cur]
            letters.append(letter)
            cur = parent
        self._shortest_path = ''.join(reversed(letters))
        return
