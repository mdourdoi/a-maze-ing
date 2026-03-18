from .Maze import Maze
from abc import ABC, abstractmethod
from typing import List, Generator
from math import ceil
import heapq
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
        if maze.body[entry[1]][entry[0]].is_ft:
            raise ValueError("The entry can't be in the 42 in the middle")
        if maze.body[out[1]][out[0]].is_ft:
            raise ValueError("The exit can't be in the 42 in the middle")
        self.name = str(name)
        self.maze = maze
        self.maze.body[entry[1]][entry[0]].is_start = True
        self.maze.body[out[1]][out[0]].is_end = True
        self.height = height
        self.wid = wid
        self.seed = seed
        self.random = random.Random(seed)

    @abstractmethod
    def generate_maze(self) -> Generator:
        pass

    def carve(self, x: int, y: int, direction: str) -> None:
        if direction == 'north':
            self.maze.body[y][x].pop_north()
            self.maze.body[y - 1][x].pop_south()
        if direction == 'south':
            self.maze.body[y][x].pop_south()
            self.maze.body[y + 1][x].pop_north()
        if direction == 'east':
            self.maze.body[y][x].pop_east()
            self.maze.body[y][x + 1].pop_west()
        if direction == 'west':
            self.maze.body[y][x].pop_west()
            self.maze.body[y][x - 1].pop_east()

    def restore(self, x: int, y: int, direction: str) -> None:
        if direction == 'north':
            self.maze.body[y][x].create_north()
            self.maze.body[y - 1][x].create_south()
        if direction == 'south':
            self.maze.body[y][x].create_south()
            self.maze.body[y + 1][x].create_north()
        if direction == 'east':
            self.maze.body[y][x].create_east()
            self.maze.body[y][x + 1].create_west()
        if direction == 'west':
            self.maze.body[y][x].create_west()
            self.maze.body[y][x - 1].create_east()

    def make_imperfect(self) -> Generator:
        to_break = ceil(self.height * self.wid / 5)
        valid_cells = [[x, y] for x in range(1, self.wid - 1)
                       for y in range(1, self.height - 1)
                       if not self.maze.body[y][x].is_ft]
        while valid_cells and to_break:
            cell = self.random.choice(valid_cells)
            walled_neighbours = self.maze.get_walled_neighbours(
                cell[0], cell[1])
            if not walled_neighbours:
                valid_cells.remove([cell[0], cell[1]])
                continue
            direction = self.random.choice(list(walled_neighbours.keys()))
            n_x, n_y = walled_neighbours[direction]
            self.carve(cell[0], cell[1], direction)
            if self.maze.is_valid():
                valid_cells.remove([cell[0], cell[1]])
                to_break -= 1
                yield [cell[0], cell[1], direction]
            else:
                self.restore(cell[0], cell[1], direction)
                valid_cells.remove([cell[0], cell[1]])

    def calculate_heuristic(self,
                            current_position: tuple(int, int),
                            next_position: tuple(int, int)) -> int:
        """ Method to calculate the heuristic value of two position """
        return sum(abs(next_position[0] - current_position[0]),
                   abs(next_position[1] - current_position[1])
        )

    def solve(self) -> Generator:
        """ Method to return a generator for the solver """
        open_set = [(self.entry[1], self.entry[0])]
        came_from = {}

        g_score = {(self.entry[1], self.entry[0]): 0}
        f_score = {(self.entry[1], self.entry[0]): self.calculate_heuristic(
            (self.entry[1], self.entry[0]),
            (self.out[1], self.out[0]))}

        while open_set:
            current = min(open_set, key=lambda x: f_score.get(x, float('inf')))

            if current == (self.end[1], self.end[0]):
                path = []
                while current in came_from:
                    path.append(current)
                    current = came_from[current]



    def find_path(self) -> Dict:
        """ Method to find the path in this """
        start_cell = tuple(self.entry[0], self.entry[1])
