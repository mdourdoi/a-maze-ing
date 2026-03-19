from .errors import WallError
from typing import Tuple


class MazeCell():

    def __init__(self,
                 north: bool = True,
                 east: bool = True,
                 south: bool = True,
                 west: bool = True,
                 is_start: bool = False,
                 is_end: bool = False,
                 is_visited: bool = False,
                 is_ft: bool = False,
                 is_solved: bool = False,
                 is_solution: bool = False) -> None:
        '''Initializes the cell.
        True means the cell has a wall in that direction'''
        self.north = north
        self.east = east
        self.south = south
        self.west = west
        self.is_start = is_start
        self.is_end = is_end
        self.is_visited = is_visited
        self.is_ft = is_ft
        self.is_solved = is_solved
        self.is_solution = is_solution

    def set_start(self) -> None:
        self.is_start = True

    def set_end(self) -> None:
        self.is_end = True

    def visit(self) -> None:
        self.is_visited = True

    def reset_g_value_update(self, g_value: int) -> None:
        """ Set g_value for this Cell and update the Score of this cell """
        self.g = g_value
        self.score = self.g + self.heuristic

    def calculate_score(self,
                        start: Tuple[int, int],
                        goal: Tuple[int, int],
                        position: Tuple[int, int]) -> None:
        """ Calculate the score and heuristic value for this cell """
        self.heuristic = abs(
            (goal[0] - position[0]) + (goal[1] - position[1])
        )
        self.score = self.g + self.heuristic

    def set_solved(self) -> None:
        """ Method to set the actual Cell to solved  """
        self.is_solved = True

    def pop_north(self) -> None:
        '''Pops the northern wall, return WallError if there is no wall'''
        if self.north:
            self.north = False
        else:
            raise WallError('The northern wall is already open')

    def pop_south(self) -> None:
        '''Pops the southern wall, return WallError if there is no wall'''
        if self.south:
            self.south = False
        else:
            raise WallError('The southern wall is already open')

    def pop_east(self) -> None:
        '''Pops the eastern wall, return WallError if there is no wall'''
        if self.east:
            self.east = False
        else:
            raise WallError('The eastern wall is already open')

    def pop_west(self) -> None:
        '''Pops the western wall, return WallError if there is no wall'''
        if self.west:
            self.west = False
        else:
            raise WallError('The western wall is already open')

    def create_north(self) -> None:
        '''Create the northern wall, return WallError if there is a wall'''
        if not self.north:
            self.north = True
        else:
            raise WallError('The northern wall already exists')

    def create_south(self) -> None:
        '''Create the southern wall, return WallError if there is a wall'''
        if not self.south:
            self.south = True
        else:
            raise WallError('The southern wall already exists')

    def create_east(self) -> None:
        '''Create the eastern wall, return WallError if there is a wall'''
        if not self.east:
            self.east = True
        else:
            raise WallError('The eastern wall already exists')

    def create_west(self) -> None:
        '''Create the western wall, return WallError if there is a wall'''
        if not self.west:
            self.west = True
        else:
            raise WallError('The western wall already exists')
