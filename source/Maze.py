from Cell import MazeCell
from typing import List, Dict


class Maze:

    def __init__(self, wid: int,
                 leng: int,
                 entry: List[int, int],
                 out: List[int, int]) -> None:
        '''Initializes a maze with all cells having 4 walls'''

        if not (isinstance(entry, list) and isinstance(out, list)):
            raise TypeError('Entry and exit must both be a list of integers')

        if not (len(entry) == 2 and len(out) == 2):
            raise TypeError(
                'Entry and exit must be a list of exactly 2 values')
        try:
            int(wid)
            int(leng)
            int(entry[0])
            int(entry[1])
            int(out[0])
            int(out[1])
        except ValueError:
            raise ValueError('All values must be integers')

        if (wid <= 0
            or leng <= 0
            or entry[0] <= 0
            or entry[1] <= 0
            or out[0] <= 0
                or out[1] <= 0):
            raise ValueError('Width and length must be strictly positive')

        if (entry[0] < 0 or entry[0] >= wid
            or entry[1] < 0 or entry[1] >= leng
            or out[0] < 0 or out[0] >= wid
                or out[1] < 0 or out[1] >= leng):
            raise ValueError('Entry and exit must be within the maze')

        if (entry[0] == out[0] and entry[1] == out[1]):
            raise ValueError('Entry and exit cannot be the same cell')

        self.body: List[List[MazeCell]] = [
            [MazeCell() for i in range(leng)] for j in range(wid)]
        self.wid: int = wid
        self.leng: int = leng
        self.entry: int = entry
        self.out: int = out

    def is_top_border(self, x: int) -> bool:
        return x == 0

    def is_bot_border(self, x: int) -> bool:
        return x == self.leng

    def is_left_border(self, y: int) -> bool:
        return y == 0

    def is_right_border(self, y: int) -> bool:
        return y == self.wid

    def get_valid_neighbours(self, x: int, y: int) -> Dict[List[int, int]]:
        res = {}
        if not (self.is_top_border(x) and self.body[x][y + 1].is_visited()):
            res['north'] = [x, y + 1]
        if not (self.is_bot_border(x) and self.body[x][y - 1].is_visited()):
            res['south'] = [x, y - 1]
        if not (self.is_left_border(y) and self.body[x + 1][y].is_visited()):
            res['west'] = [x - 1, y]
        if not (self.is_right_border(y) and self.body[x - 1][y].is_visited()):
            res['east'] = [x + 1, y]
