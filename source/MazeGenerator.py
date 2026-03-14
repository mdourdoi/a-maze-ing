from .Maze import Maze
from abc import ABC, abstractmethod
from typing import List, Generator
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
