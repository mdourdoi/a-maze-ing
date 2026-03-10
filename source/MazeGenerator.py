from .Maze import Maze
from abc import ABC, abstractmethod
from typing import List
import random


class MazeGenerator(ABC):

    def __init__(self,
                 name: str,
                 entry: List[int],
                 out: List[int],
                 wid: int,
                 leng: int,
                 seed: int | None = None):
        if not str(name):
            raise ValueError('Please input a valid name')
        self.name = str(name)
        self.maze = Maze(wid, leng, entry, out)
        self.wid = wid
        self.leng = leng
        self.seed = seed
        self.random = random.Random(seed)

    @abstractmethod
    def generate_maze(self, x: int, y: int) -> None:
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
