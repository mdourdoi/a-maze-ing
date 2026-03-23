from .errors import WallError


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
        self._is_visited = is_visited
        self.is_ft = is_ft
        self.is_solved = is_solved
        self._is_solution = is_solution

    def _visit(self) -> None:
        self._is_visited = True

    def _get_bin_value(self) -> int:
        value: int = 0
        if self.north:
            value += 1
        if self.east:
            value += 2
        if self.south:
            value += 4
        if self.west:
            value += 8
        return value

    def _set_solved(self) -> None:
        """ Method to set the actual Cell to solved  """
        self.is_solved = True

    def _pop_north(self) -> None:
        '''Pops the northern wall, return WallError if there is no wall'''
        if self.north:
            self.north = False
        else:
            raise WallError('The northern wall is already open')

    def _pop_south(self) -> None:
        '''Pops the southern wall, return WallError if there is no wall'''
        if self.south:
            self.south = False
        else:
            raise WallError('The southern wall is already open')

    def _pop_east(self) -> None:
        '''Pops the eastern wall, return WallError if there is no wall'''
        if self.east:
            self.east = False
        else:
            raise WallError('The eastern wall is already open')

    def _pop_west(self) -> None:
        '''Pops the western wall, return WallError if there is no wall'''
        if self.west:
            self.west = False
        else:
            raise WallError('The western wall is already open')

    def _create_north(self) -> None:
        '''Create the northern wall, return WallError if there is a wall'''
        if not self.north:
            self.north = True
        else:
            raise WallError('The northern wall already exists')

    def _create_south(self) -> None:
        '''Create the southern wall, return WallError if there is a wall'''
        if not self.south:
            self.south = True
        else:
            raise WallError('The southern wall already exists')

    def _create_east(self) -> None:
        '''Create the eastern wall, return WallError if there is a wall'''
        if not self.east:
            self.east = True
        else:
            raise WallError('The eastern wall already exists')

    def _create_west(self) -> None:
        '''Create the western wall, return WallError if there is a wall'''
        if not self.west:
            self.west = True
        else:
            raise WallError('The western wall already exists')
