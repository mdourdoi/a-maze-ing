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
                 is_ft: bool = False) -> None:
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

    def set_start(self) -> None:
        self.is_start = True

    def set_end(self) -> None:
        self.is_end = True

    def visit(self) -> None:
        self.is_visited = True

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
