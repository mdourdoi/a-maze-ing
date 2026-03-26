from .Cell import MazeCell
from typing import List, Dict


class Maze:
    """Represent a maze grid, its cells, and neighbourhood queries."""

    def __init__(self, height: int,
                 wid: int,
                 entry: List[int],
                 out: List[int],
                 verbose: bool = False) -> None:
        """Initialize a maze whose cells all start with four walls.

        Args:
            height: Maze height in number of cells.
            wid: Maze width in number of cells.
            entry: Entry cell coordinates as [x, y].
            out: Exit cell coordinates as [x, y].

        Returns:
            None: This constructor initializes the maze in place.
        """

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
        self.body[entry[1]][entry[0]].is_start = True
        self.body[out[1]][out[0]].is_end = True
        self.__set_forty_two_pattern(verbose)
        if self.body[entry[1]][entry[0]]._is_ft:
            raise ValueError("The entry can't be in the 42 in the middle")
        if self.body[out[1]][out[0]]._is_ft:
            raise ValueError("The exit can't be in the 42 in the middle")

    def is_top_border(self, y: int) -> bool:
        """Check whether a row index lies on the top border.

        Args:
            y: Row index to test.

        Returns:
            bool: True when the row is the first row of the maze.
        """
        return y == 0

    def is_bot_border(self, y: int) -> bool:
        """Check whether a row index lies on the bottom border.

        Args:
            y: Row index to test.

        Returns:
            bool: True when the row is the last row of the maze.
        """
        return y == self.height - 1

    def is_left_border(self, x: int) -> bool:
        """Check whether a column index lies on the left border.

        Args:
            x: Column index to test.

        Returns:
            bool: True when the column is the first column of the maze.
        """
        return x == 0

    def is_right_border(self, x: int) -> bool:
        """Check whether a column index lies on the right border.

        Args:
            x: Column index to test.

        Returns:
            bool: True when the column is the last column of the maze.
        """
        return x == self.wid - 1

    def _get_valid_neighbours(self, x: int, y: int) -> Dict[str, List[int]]:
        """Return unvisited neighbours that can be carved next.

        Args:
            x: Horizontal index of the source cell.
            y: Vertical index of the source cell.

        Returns:
            Dict[str, List[int]]: Mapping of directions to neighbour
            coordinates that are inside the maze, unvisited, and not part of
            the 42 pattern.
        """
        res = {}
        if (not self.is_top_border(y)
            and not self.body[y - 1][x]._is_visited
                and not self.body[y - 1][x]._is_ft):
            res['north'] = [x, y - 1]
        if (not self.is_bot_border(y)
            and not self.body[y + 1][x]._is_visited
                and not self.body[y + 1][x]._is_ft):
            res['south'] = [x, y + 1]
        if (not self.is_right_border(x)
            and not self.body[y][x + 1]._is_visited
                and not self.body[y][x + 1]._is_ft):
            res['east'] = [x + 1, y]
        if (not self.is_left_border(x)
            and not self.body[y][x - 1]._is_visited
                and not self.body[y][x - 1]._is_ft):
            res['west'] = [x - 1, y]
        return res

    def _get_visited_neighbours(self, x: int, y: int) -> Dict[str, List[int]]:
        """Return already visited neighbours around a cell.

        Args:
            x: Horizontal index of the source cell.
            y: Vertical index of the source cell.

        Returns:
            Dict[str, List[int]]: Mapping of directions to neighbour
            coordinates that have already been visited.
        """
        res = {}
        if (not self.is_top_border(y)
            and self.body[y - 1][x]._is_visited
                and not self.body[y - 1][x]._is_ft):
            res['north'] = [x, y - 1]
        if (not self.is_bot_border(y)
            and self.body[y + 1][x]._is_visited
                and not self.body[y + 1][x]._is_ft):
            res['south'] = [x, y + 1]
        if (not self.is_right_border(x)
            and self.body[y][x + 1]._is_visited
                and not self.body[y][x + 1]._is_ft):
            res['east'] = [x + 1, y]
        if (not self.is_left_border(x)
            and self.body[y][x - 1]._is_visited
                and not self.body[y][x - 1]._is_ft):
            res['west'] = [x - 1, y]
        return res

    def _get_walled_neighbours(self, x: int, y: int) -> Dict[str, List[int]]:
        """Return adjacent neighbours still separated by walls.

        Args:
            x: Horizontal index of the source cell.
            y: Vertical index of the source cell.

        Returns:
            Dict[str, List[int]]: Mapping of directions to neighbouring cells
            whose shared wall is still closed.
        """
        res = {}
        if (not self.is_top_border(y)
            and self.body[y - 1][x].south
            and self.body[y][x].north
                and not self.body[y - 1][x]._is_ft):
            res['north'] = [x, y - 1]
        if (not self.is_bot_border(y)
            and self.body[y + 1][x].north
            and self.body[y][x].south
                and not self.body[y + 1][x]._is_ft):
            res['south'] = [x, y + 1]
        if (not self.is_right_border(x)
            and self.body[y][x + 1].west
            and self.body[y][x].east
                and not self.body[y][x + 1]._is_ft):
            res['east'] = [x + 1, y]
        if (not self.is_left_border(x)
            and self.body[y][x - 1].east
            and self.body[y][x].west
                and not self.body[y][x - 1]._is_ft):
            res['west'] = [x - 1, y]
        return res

    def _get_unsolved_neighbours(self,
                                 x: int,
                                 y: int) -> Dict[str, tuple[int, int]]:
        """Return reachable neighbouring cells not yet marked as solved.

        Args:
            x: Horizontal index of the source cell.
            y: Vertical index of the source cell.

        Returns:
            Dict[str, tuple[int, int]]: Mapping of directions to reachable
            neighbours available to the solver.
        """
        res = {}
        if (not self.is_top_border(y)
            and not self.body[y - 1][x]._is_solved
                and not self.body[y][x]._is_ft
                and not self.body[y - 1][x].south
                and not self.body[y][x].north):
            res['north'] = (x, y - 1)
        if (not self.is_bot_border(y)
            and not self.body[y + 1][x]._is_solved
                and not self.body[y + 1][x]._is_ft
                and not self.body[y + 1][x].north
                and not self.body[y][x].south):
            res['south'] = (x, y + 1)
        if (not self.is_right_border(x)
            and not self.body[y][x + 1]._is_solved
                and not self.body[y][x + 1]._is_ft
                and not self.body[y][x + 1].west
                and not self.body[y][x].east):
            res['east'] = (x + 1, y)
        if (not self.is_left_border(x)
            and not self.body[y][x - 1]._is_solved
                and not self.body[y][x - 1]._is_ft
                and not self.body[y][x - 1].east
                and not self.body[y][x].west):
            res['west'] = (x - 1, y)
        return res

    def __set_forty_two_pattern(self, verbose: bool = False) -> None:
        """Mark the central 42 pattern cells when the maze is large enough.

        Returns:
            None: This method updates maze cells in place.
        """
        pattern = [
            "1   222",
            "1     2",
            "111 222",
            "  1 2  ",
            "  1 222"
        ]
        if self.wid <= 7 or self.height <= 5:
            if verbose:
                print('Not enough space for the 42 pattern.', end='')
                print('Continuing without ...')
            return
        start_x = (self.wid - 7) // 2
        start_y = (self.height - 5) // 2
        for j in range(5):
            for i in range(7):
                if pattern[j][i] != ' ':
                    self.body[start_y + j][start_x + i]._is_ft = True

    def __is_open_vertically(self, x: int, y: int) -> bool:
        """Check whether two vertically adjacent cells are connected.

        Args:
            x: Column index of the upper cell.
            y: Row index of the upper cell.

        Returns:
            bool: True when the shared vertical passage is open.
        """
        return not self.body[y][x].south and not self.body[y + 1][x].north

    def __is_open_horizontally(self, x: int, y: int) -> bool:
        """Check whether two horizontally adjacent cells are connected.

        Args:
            x: Column index of the left cell.
            y: Row index of the left cell.

        Returns:
            bool: True when the shared horizontal passage is open.
        """
        return not self.body[y][x].east and not self.body[y][x + 1].west

    def __is_valid_cell(self, x: int, y: int) -> bool:
        """Check local wall structure around a cell for validity.

        Args:
            x: Horizontal index of the cell to inspect.
            y: Vertical index of the cell to inspect.

        Returns:
            bool: True when the local neighbourhood does not create an invalid
            open area.
        """
        for i in range(3):
            for j in range(2):
                if not (self.__is_open_horizontally(x - 1 + j, y - 1 + i)):
                    return True
        for i in range(3):
            for j in range(2):
                if not (self.__is_open_vertically(x - 1 + i, y - 1 + j)):
                    return True
        return False

    def _is_valid(self) -> bool:
        """Validate the maze by checking every non-border cell.

        Returns:
            bool: True when the maze satisfies the local validity rules.
        """
        for y in range(1, self.height - 1):
            for x in range(1, self.wid - 1):
                if not self.__is_valid_cell(x, y):
                    return False
        return True
