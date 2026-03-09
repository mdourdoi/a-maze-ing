from Maze import Maze
from abc import ABC, abstractmethod


class MazeGenerator(ABC):

    def __init__(self, name: str):
        if not str(name):
            raise ValueError('Please input a valid name')
        self.name = str(name)

    @abstractmethod
    def generate_maze(self) -> Maze:
        pass
