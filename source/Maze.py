from .Cell import MazeCell
from typing import List, Dict


class Maze:

    def __init__(self, height: int,
                 wid: int,
                 entry: List[int],
                 out: List[int]) -> None:
        '''Initializes a maze with all cells having 4 walls'''

        if not (isinstance(entry, list) and isinstance(out, list)):
            raise TypeError('Entry and exit must both be a list of integers')

        if not (len(entry) == 2 and len(out) == 2):
            raise TypeError(
                'Entry and exit must be a list of exactly 2 values')
        try:
            int(height)
            int(wid)
            int(entry[0])
            int(entry[1])
            int(out[0])
            int(out[1])
        except ValueError:
            raise ValueError('All values must be integers')

        if (height <= 0 or wid <= 0):
            raise ValueError('Width and length must be strictly positive')

        if (entry[0] < 0 or entry[0] >= wid
            or entry[1] < 0 or entry[1] >= height
            or out[0] < 0 or out[0] >= wid
                or out[1] < 0 or out[1] >= height):
            raise ValueError('Entry and exit must be within the maze')

        if (entry[0] == out[0] and entry[1] == out[1]):
            raise ValueError('Entry and exit cannot be the same cell')

        self.body: List[List[MazeCell]] = [
            [MazeCell() for i in range(wid)] for j in range(height)]
        self.height: int = height
        self.wid: int = wid
        self.entry: List[int] = entry
        self.out: List[int] = out
        self.__set_forty_two_pattern()

    def is_top_border(self, y: int) -> bool:
        return y == 0

    def is_bot_border(self, y: int) -> bool:
        return y == self.height - 1

    def is_left_border(self, x: int) -> bool:
        return x == 0

    def is_right_border(self, x: int) -> bool:
        return x == self.wid - 1

    def get_valid_neighbours(self, x: int, y: int) -> Dict[str, List[int]]:
        res = {}
        if (not self.is_top_border(y)
            and not self.body[y - 1][x].is_visited
                and not self.body[y - 1][x].is_ft):
            res['north'] = [x, y - 1]
        if (not self.is_bot_border(y)
            and not self.body[y + 1][x].is_visited
                and not self.body[y + 1][x].is_ft):
            res['south'] = [x, y + 1]
        if (not self.is_right_border(x)
            and not self.body[y][x + 1].is_visited
                and not self.body[y][x + 1].is_ft):
            res['east'] = [x + 1, y]
        if (not self.is_left_border(x)
            and not self.body[y][x - 1].is_visited
                and not self.body[y][x - 1].is_ft):
            res['west'] = [x - 1, y]
        return res

    def get_visited_neighbours(self, x: int, y: int) -> Dict[str, List[int]]:
        res = {}
        if (not self.is_top_border(y)
            and self.body[y - 1][x].is_visited
                and not self.body[y - 1][x].is_ft):
            res['north'] = [x, y - 1]
        if (not self.is_bot_border(y)
            and self.body[y + 1][x].is_visited
                and not self.body[y + 1][x].is_ft):
            res['south'] = [x, y + 1]
        if (not self.is_right_border(x)
            and self.body[y][x + 1].is_visited
                and not self.body[y][x + 1].is_ft):
            res['east'] = [x + 1, y]
        if (not self.is_left_border(x)
            and self.body[y][x - 1].is_visited
                and not self.body[y][x - 1].is_ft):
            res['west'] = [x - 1, y]
        return res

    def get_walled_neighbours(self, x: int, y: int) -> Dict[str, List[int]]:
        res = {}
        if (not self.is_top_border(y)
            and self.body[y - 1][x].south
            and self.body[y][x].north
                and not self.body[y][x].is_ft):
            res['north'] = [x, y - 1]
        if (not self.is_bot_border(y)
            and self.body[y + 1][x].north
            and self.body[y][x].south
                and not self.body[y][x].is_ft):
            res['south'] = [x, y + 1]
        if (not self.is_right_border(x)
            and self.body[y][x + 1].west
            and self.body[y][x].east
                and not self.body[y][x + 1].is_ft):
            res['east'] = [x + 1, y]
        if (not self.is_left_border(x)
            and self.body[y][x - 1].east
            and self.body[y][x].west
                and not self.body[y][x - 1].is_ft):
            res['west'] = [x - 1, y]
        return res

    def calculate_heuristic(self,
                            current_position: tuple(int, int),
                            next_position: tuple(int, int)) -> int:
        """ Method to calculate the heuristic value of two position """
        return sum(abs(next_position[0] - current_position[0]),
                   abs(next_position[1] - current_position[1])
        )

    def get_unsolved_neighbours(self,
                                x: int,
                                y: int) -> List[tuple(int, int, str)]:
        """ Return a Dict with the unsolved Cell from a position """
        res: List[tuple(int, int, str)] = []
        if (not self.is_top_border(y)
            and not self.body[y - 1][x].is_solved
                and not self.body[y - 1][x].is_ft
                    and not self.body[y - 1][x].north):
            res.append(tuple(x, y - 1, "north"))
        if (not self.is_bot_border(y)
            and not self.body[y + 1][x].is_solved
                and not self.body[y + 1][x].is_ft
                    and not self.body[y + 1][x].south):
            res.append(tuple(x, y + 1, "south"))
        if (not self.is_right_border(x)
            and not self.body[y][x + 1].is_solved
                and not self.body[y][x + 1].is_ft
                    and not self.body[y][x + 1].east):
            res.append(tuple(x + 1, y, "east"))
        if (not self.is_left_border(x)
            and not self.body[y][x - 1].is_solved
                and not self.body[y][x - 1].is_ft
                    and not self.body[y][x - 1].west):
            res.append(tuple(x - 1, y, "west"))
        return res

    def __set_cost_score(self) -> None:
        """ Set the score of each Cell of the maze for the solving """
        for x in self.body:
            for y in x:
                y.calculate_score()

    def __set_forty_two_pattern(self) -> None:
        pattern = [
            "1   222",
            "1     2",
            "111 222",
            "  1 2  ",
            "  1 222"
        ]
        if self.wid < 7 or self.height < 5:
            print('Not enough space to put the 42 pattern, continuing without')
            return
        start_x = (self.wid - 7) // 2
        start_y = (self.height - 5) // 2
        for j in range(5):
            for i in range(7):
                if pattern[j][i] != ' ':
                    self.body[start_y + j][start_x + i].is_ft = True

    def __is_open_vertically(self, x: int, y: int) -> bool:
        return not self.body[y][x].south and not self.body[y + 1][x].north

    def __is_open_horizontally(self, x: int, y: int) -> bool:
        return not self.body[y][x].east and not self.body[y][x + 1].west

    def is_valid_cell(self, x: int, y: int) -> bool:
        for i in range(3):
            for j in range(2):
                if not (self.__is_open_horizontally(x - 1 + j, y - 1 + i)):
                    return True
        for i in range(3):
            for j in range(2):
                if not (self.__is_open_vertically(x - 1 + i, y - 1 + j)):
                    return True
        return False

    def is_valid(self) -> bool:
        for y in range(1, self.height - 1):
            for x in range(1, self.wid - 1):
                if not self.is_valid_cell(x, y):
                    return False
        return True
