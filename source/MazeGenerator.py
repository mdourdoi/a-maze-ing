from .Maze import Maze
from abc import ABC, abstractmethod
from typing import List, Generator, Tuple, Dict
import random


class MazeGenerator(ABC):
    """Base class for maze generation, solving, and export workflows."""

    def __init__(self,
                 name: str,
                 entry: List[int],
                 out: List[int],
                 height: int,
                 wid: int,
                 seed: int | None = None):
        """Initialize a maze generator and its shared runtime state.

        Args:
            name: Human-readable name of the generator.
            entry: Entry cell coordinates as [x, y].
            out: Exit cell coordinates as [x, y].
            height: Maze height in number of cells.
            wid: Maze width in number of cells.
            seed: Optional seed used for deterministic randomness.

        Returns:
            None: This constructor initializes the instance in place.
        """
        if not str(name):
            raise ValueError('Please input a valid name')
        maze = Maze(height, wid, entry, out, True)
        self.entry = entry
        self.out = out
        self.name = str(name)
        self.maze = maze
        self.height = height
        self.wid = wid
        self.seed = seed
        self._random = random.Random(seed)
        self.is_solved = False
        self.is_generated = False
        self.solution: List[Tuple[int, int]] = []

    @abstractmethod
    def _generate_maze(self) -> Generator[List[int], None, None]:
        """Yield generation steps until the maze structure is complete.

        Returns:
            Generator[List[int], None, None]: A generator yielding the
            coordinates of cells updated during generation.
        """
        pass

    def _carve(self, x: int, y: int, direction: str) -> None:
        """Open a wall between a cell and one of its neighbours.

        Args:
            x: Horizontal index of the source cell.
            y: Vertical index of the source cell.
            direction: Direction of the neighbouring cell to connect.

        Returns:
            None: This method mutates the maze walls in place.
        """
        if direction == 'north':
            self.maze.body[y][x]._pop_north()
            self.maze.body[y - 1][x]._pop_south()
        if direction == 'south':
            self.maze.body[y][x]._pop_south()
            self.maze.body[y + 1][x]._pop_north()
        if direction == 'east':
            self.maze.body[y][x]._pop_east()
            self.maze.body[y][x + 1]._pop_west()
        if direction == 'west':
            self.maze.body[y][x]._pop_west()
            self.maze.body[y][x - 1]._pop_east()

    def _restore(self, x: int, y: int, direction: str) -> None:
        """Restore a wall previously removed between two adjacent cells.

        Args:
            x: Horizontal index of the source cell.
            y: Vertical index of the source cell.
            direction: Direction of the neighbouring cell to disconnect.

        Returns:
            None: This method mutates the maze walls in place.
        """
        if direction == 'north':
            self.maze.body[y][x]._create_north()
            self.maze.body[y - 1][x]._create_south()
        if direction == 'south':
            self.maze.body[y][x]._create_south()
            self.maze.body[y + 1][x]._create_north()
        if direction == 'east':
            self.maze.body[y][x]._create_east()
            self.maze.body[y][x + 1]._create_west()
        if direction == 'west':
            self.maze.body[y][x]._create_west()
            self.maze.body[y][x - 1]._create_east()

    def __entry_out_are_adjacent(self) -> bool:
        """Check whether the entry and exit cells share a side."""
        return (abs(self.maze.entry[0] - self.maze.out[0]) +
                abs(self.maze.entry[1] - self.maze.out[1])) == 1

    def __square_contains_entry_and_out(self, top_left_x: int,
                                        top_left_y: int) -> bool:
        """Check whether a 2x2 square contains both entry and exit cells."""
        square_cells = {
            (top_left_x, top_left_y),
            (top_left_x + 1, top_left_y),
            (top_left_x, top_left_y + 1),
            (top_left_x + 1, top_left_y + 1)
        }
        return ((self.maze.entry[0], self.maze.entry[1]) in square_cells
                and (self.maze.out[0], self.maze.out[1]) in square_cells)

    def __try_open_entry_exit_loop(self) -> List[List[int]]:
        """Try to create a valid 2x2 loop containing entry and exit.

        Returns:
            List[List[int]]: Source cells whose walls were effectively opened.
        """
        if not self.__entry_out_are_adjacent():
            return []
        min_x = min(self.maze.entry[0], self.maze.out[0])
        max_x = max(self.maze.entry[0], self.maze.out[0])
        min_y = min(self.maze.entry[1], self.maze.out[1])
        max_y = max(self.maze.entry[1], self.maze.out[1])
        candidates: List[Tuple[int, int]] = []
        for top_left_x in range(min_x - 1, max_x + 1):
            for top_left_y in range(min_y - 1, max_y + 1):
                if (top_left_x < 0 or top_left_y < 0
                        or top_left_x + 1 >= self.wid
                        or top_left_y + 1 >= self.height):
                    continue
                if not self.__square_contains_entry_and_out(
                        top_left_x, top_left_y):
                    continue
                if any(self.maze.body[y][x]._is_ft
                       for x in range(top_left_x, top_left_x + 2)
                       for y in range(top_left_y, top_left_y + 2)):
                    continue
                candidates.append((top_left_x, top_left_y))
        self._random.shuffle(candidates)
        for top_left_x, top_left_y in candidates:
            perimeter_edges = [
                (top_left_x, top_left_y, 'east'),
                (top_left_x + 1, top_left_y, 'south'),
                (top_left_x, top_left_y + 1, 'east'),
                (top_left_x, top_left_y, 'south')
            ]
            opened_edges: List[Tuple[int, int, str]] = []
            opened_cells: List[List[int]] = []
            for x, y, direction in perimeter_edges:
                if direction not in self.maze._get_walled_neighbours(x, y):
                    continue
                self._carve(x, y, direction)
                opened_edges.append((x, y, direction))
                opened_cells.append([x, y])
            if opened_edges and self.maze._is_valid():
                return opened_cells
            for x, y, direction in reversed(opened_edges):
                self._restore(x, y, direction)
        return []

    def _make_imperfect(self) -> Generator[List[int], None, None]:
        """Break additional walls to create loops in the generated maze.
        At least one wall is broken each time, and at most 20%.

        Returns:
            Generator[List[int], None, None]: A generator yielding the
            coordinates of cells modified while relaxing the maze.
        """

        to_break = self.height * self.wid // 5
        opened_entry_exit_loop = self.__try_open_entry_exit_loop()
        if opened_entry_exit_loop:
            to_break = max(0, to_break - len(opened_entry_exit_loop))
            for cell in opened_entry_exit_loop:
                yield cell
        valid_cells = [[x, y] for x in range(self.wid)
                       for y in range(self.height)
                       if not self.maze.body[y][x]._is_ft]
        broke_at_least_one = bool(opened_entry_exit_loop)
        while valid_cells and (to_break or not broke_at_least_one):
            cell = self._random.choice(valid_cells)
            walled_neighbours = self.maze._get_walled_neighbours(
                cell[0], cell[1])
            if not walled_neighbours:
                valid_cells.remove([cell[0], cell[1]])
                continue
            direction = self._random.choice(list(walled_neighbours.keys()))
            self._carve(cell[0], cell[1], direction)
            if self.maze._is_valid():
                valid_cells.remove([cell[0], cell[1]])
                to_break -= 1
                broke_at_least_one = True
                yield [cell[0], cell[1]]
            else:
                self._restore(cell[0], cell[1], direction)
                valid_cells.remove([cell[0], cell[1]])

    def __calculate_heuristic(self,
                              current_position: Tuple[int, int],
                              next_position: Tuple[int, int]) -> float:
        """Compute the Manhattan distance between two positions.

        Args:
            current_position: Starting position as an (x, y) tuple.
            next_position: Target position as an (x, y) tuple.

        Returns:
            float: Heuristic distance used by the solver.
        """
        return abs(next_position[0] - current_position[0]) + \
            abs(next_position[1] - current_position[1])

    def _solve(self) -> Generator[Tuple[int, int], None, None]:
        """Solve the maze and yield visited or solution cells step by step.

        Returns:
            Generator[Tuple[int, int], None, None]: A generator yielding cell
            coordinates as the search progresses and when the final path is
            reconstructed.
        """
        open_list = [(self.maze.entry[0], self.maze.entry[1])]
        came_from: Dict[Tuple[int, int], Tuple[int, int]] = {}

        g_score = {(self.maze.entry[0], self.maze.entry[1]): 0}
        f_score = {(self.maze.entry[0], self.maze.entry[1]):
                   self.__calculate_heuristic(
            (self.maze.entry[0], self.maze.entry[1]),
            (self.maze.out[0], self.maze.out[1]))}

        while open_list:
            current = min(
                open_list, key=lambda x: f_score[x])
            self.maze.body[current[1]][current[0]]._set_solved()

            if current == (self.maze.out[0], self.maze.out[1]):
                self.is_solved = True
                self.maze.body[current[1]][current[0]]._set_solved()
                path = []
                while current in came_from:
                    path.append(current)
                    current = came_from[current]
                path.append((self.maze.entry[0], self.maze.entry[1]))
                self.solution = list(reversed(path))
                for data in self.solution:
                    self.maze.body[data[1]][data[0]]._is_solution = True
                    yield (data[0], data[1])
                return

            open_list.remove(current)
            for neighbor in self.maze._get_unsolved_neighbours(
                    current[0], current[1]).values():
                tentative_g = g_score[current] + 1

                if tentative_g < g_score.get(neighbor, float('inf')):
                    came_from[neighbor] = current
                    g_score[neighbor] = tentative_g
                    f_score[neighbor] = tentative_g
                    f_score[neighbor] += self.__calculate_heuristic(
                        (neighbor[0], neighbor[1]),
                        (self.maze.out[0], self.maze.out[1]))

                    if (neighbor[0], neighbor[1]) not in open_list:
                        open_list.append((neighbor[0], neighbor[1]))
            yield ((current[0], current[1]))

    def __solution_string(self) -> str:
        """Convert the solved path into cardinal movement instructions.

        Returns:
            str: A compact string made of N, S, E, and W directions.
        """
        res: str = ""
        for i in range(len(self.solution) - 1):
            if (self.solution[i][0] - self.solution[i + 1][0]) != 0:
                if (self.solution[i][0] - self.solution[i + 1][0]) > 0:
                    res = "".join([res, "W"])
                else:
                    res = "".join([res, "E"])
            if (self.solution[i][1] - self.solution[i + 1][1]) != 0:
                if (self.solution[i][1] - self.solution[i + 1][1]) > 0:
                    res = "".join([res, "N"])
                else:
                    res = "".join([res, "S"])
        return res

    def _output(self, filename: str, verbose: bool = True) -> None:
        """Write the maze grid, endpoints, and solution path to a file.

        Args:
            filename: Path of the output file to create or overwrite.
            verbose: Whether to print status messages during export.

        Returns:
            None: This method writes the serialized maze to disk.
        """
        try:
            with open(filename, "r+") as f:
                if verbose:
                    print(f"{filename} already exists, overwriting...")
                f.seek(0)
                f.truncate()
        except (FileNotFoundError):
            if verbose:
                print(f"Creating {filename}...")
        try:
            with open(filename, "a") as f:
                for y in range(self.maze.height):
                    line: str = ""
                    for x in range(self.maze.wid):
                        line = ''.join(
                            [line,
                             f"{hex(self.maze.body[y][x]._get_bin_value())}"])
                    line = line.replace("0x", "")
                    line = line.upper()
                    f.write(line)
                    f.write("\n")
                f.write(f"\n{self.maze.entry[0]},{self.maze.entry[1]}")
                f.write(f"\n{self.maze.out[0]},{self.maze.out[1]}\n")
                f.write(self.__solution_string())
        except Exception as e:
            print(f"Error while writing output file: {e}")

    def reset_maze(self) -> None:
        """Reset the maze and clear generation and solving state.

        Returns:
            None: This method replaces the current maze in place.
        """
        self.maze = Maze(self.height, self.wid, self.entry, self.out)
        self.is_solved = False
        self.is_generated = False
        self.solution = []

    def create_full_maze(
            self,
            filename: str,
            perfect: bool,
            export: bool = False) -> None:
        """Generate, solve, and optionally export a complete maze.

        Args:
            filename: Output file used when export is enabled.
            perfect: Whether to keep the maze perfect or add extra openings.
            export: Whether to serialize the final maze to a file.

        Returns:
            None: This method drives the full maze lifecycle in place.
        """
        if not self.is_generated:
            creator = self._generate_maze()
            while not self.is_generated:
                try:
                    next(creator)
                except StopIteration:
                    if not perfect:
                        imperfector = self._make_imperfect()
                        while True:
                            try:
                                next(imperfector)
                            except StopIteration:
                                break
                    self.is_generated = True
        if not self.is_solved:
            solver = self._solve()
            while not self.is_solved:
                try:
                    next(solver)
                except StopIteration:
                    self.is_solved = True
                    break
        if export:
            self._output(filename, False)

    @classmethod
    def basic_example(cls) -> "MazeGenerator":
        """Build a ready-to-use imperfect maze example.

        Returns:
            MazeGenerator: A generated example instance of the concrete class.
        """
        generator = cls(
            name=f"{cls.__name__} basic example",
            entry=[0, 0],
            out=[19, 14],
            height=15,
            wid=20,
            seed=None)
        generator.create_full_maze("", perfect=False, export=False)
        return generator
