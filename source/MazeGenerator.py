from .Maze import Maze
from abc import ABC, abstractmethod
from typing import List, Generator, Tuple
from math import ceil
import random


class MazeGenerator(ABC):

    def __init__(self,
                 name: str,
                 entry: List[int],
                 out: List[int],
                 height: int,
                 wid: int,
                 seed: int | None = None):
        if not str(name):
            raise ValueError('Please input a valid name')
        maze = Maze(height, wid, entry, out)
        self.entry = entry
        self.out = out
        self.name = str(name)
        self.maze = maze
        self.maze.body[entry[1]][entry[0]].is_start = True
        self.maze.body[out[1]][out[0]].is_end = True
        self.height = height
        self.wid = wid
        self.seed = seed
        self._random = random.Random(seed)
        self.is_solved = False
        self.is_generated = False
        self.solution = []

    @abstractmethod
    def _generate_maze(self) -> Generator:
        pass

    def _carve(self, x: int, y: int, direction: str) -> None:
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
            self.maze.body[y][x - 1].create_east()

    def _make_imperfect(self) -> Generator:
        to_break = ceil(self.height * self.wid / 5)
        valid_cells = [[x, y] for x in range(self.wid)
                       for y in range(self.height)
                       if not self.maze.body[y][x]._is_ft]
        while valid_cells and to_break:
            cell = self._random.choice(valid_cells)
            walled_neighbours = self.maze._get_walled_neighbours(
                cell[0], cell[1])
            if not walled_neighbours:
                valid_cells.remove([cell[0], cell[1]])
                continue
            direction = self._random.choice(list(walled_neighbours.keys()))
            n_x, n_y = walled_neighbours[direction]
            self._carve(cell[0], cell[1], direction)
            if self.maze._is_valid():
                valid_cells.remove([cell[0], cell[1]])
                to_break -= 1
                yield [cell[0], cell[1], direction]
            else:
                self._restore(cell[0], cell[1], direction)
                valid_cells.remove([cell[0], cell[1]])

    def __calculate_heuristic(self,
                              current_position: Tuple[int, int],
                              next_position: Tuple[int, int]) -> float:
        """ Method to calculate the heuristic value of two position """
        return abs(next_position[0] - current_position[0]) + \
            abs(next_position[1] - current_position[1])

    def _solve(self) -> Generator:
        """ Method to return a generator for the solver """
        open_list = [(self.maze.entry[0], self.maze.entry[1])]
        came_from = {}

        g_score = {(self.maze.entry[0], self.maze.entry[1]): 0}
        f_score = {(self.maze.entry[0], self.maze.entry[1]):
                   self.__calculate_heuristic(
            (self.maze.entry[0], self.maze.entry[1]),
            (self.maze.out[0], self.maze.out[1]))}

        while open_list:
            current = min(
                open_list, key=lambda x: f_score.get(x))
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
        """Generate a formated string with the directions of the solution"""
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
        """ Method to output the maze body into a file """
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
            print({e})

    def reset_maze(self):
        self.maze = Maze(self.height, self.wid, self.entry, self.out)
        self.is_solved = False
        self.is_generated = False
        self.solution = []

    def create_full_maze(
            self,
            filename: str,
            perfect: bool,
            export: bool = False) -> None:
        """ Generates the maze, renders it imperfect is perfect is set to
        False, then exports the filename """
        if not self.is_generated:
            creator = self._generate_maze()
            while not self.is_generated:
                try:
                    next(creator)
                except StopIteration:
                    if not perfect:
                        self._make_imperfect()
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
