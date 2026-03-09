from Cell import MazeCell
from typing import List


class Maze:

    def __init__(self, wid: int, leng: int) -> None:
        '''Initializes a maze with all cells having 4 walls'''
        self.body = [[MazeCell() for i in range(leng)] for j in range(wid)]

    @staticmethod
    def is_border(x: int, y: int) -> bool:

    def get_valid_neighbours(self, x: int, y: int) -> List[List[int, int]]:
        res = []
        if
