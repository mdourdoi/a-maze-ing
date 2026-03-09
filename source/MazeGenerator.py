from Maze import Maze
from abc import ABC, abstractmethod
from typing import List


class MazeGenerator(ABC):

    def __init__(self,
                 name: str,
                 entry: List[int, int],
                 out: List[int, int],
                 wid: int,
                 leng: int):
        if not str(name):
            raise ValueError('Please input a valid name')
        self.name = str(name)
        self.maze = Maze(wid, leng, entry, out)

    @abstractmethod
    def generate_maze(self, x: int, y: int) -> Maze:
        pass
