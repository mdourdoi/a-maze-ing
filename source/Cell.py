from .errors import WallError


class MazeCell():
    """Represent a maze cell, its walls, and traversal state."""

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
        """Initialize a cell with its walls and state flags.

        Args:
            north: Whether the north wall exists.
            east: Whether the east wall exists.
            south: Whether the south wall exists.
            west: Whether the west wall exists.
            is_start: Whether the cell is the maze entry.
            is_end: Whether the cell is the maze exit.
            is_visited: Whether the cell has been visited by generation.
            is_ft: Whether the cell belongs to the 42 pattern.
            is_solved: Whether the solver has already processed the cell.
            is_solution: Whether the cell belongs to the final solution path.

        Returns:
            None: This constructor initializes the cell in place.
        """
        self.north = north
        self.east = east
        self.south = south
        self.west = west
        self.is_start = is_start
        self.is_end = is_end
        self._is_visited = is_visited
        self._is_ft = is_ft
        self._is_solved = is_solved
        self._is_solution = is_solution

    def _visit(self) -> None:
        """Mark the cell as visited by a generation algorithm.

        Returns:
            None: This method updates the cell state in place.
        """
        self._is_visited = True

    def _get_bin_value(self) -> int:
        """Encode the current wall layout as a bitmask value.

        Returns:
            int: Integer value representing the four wall states.
        """
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
        """Mark the cell as processed by the solver.

        Returns:
            None: This method updates the cell state in place.
        """
        self._is_solved = True

    def _pop_north(self) -> None:
        """Remove the north wall of the cell.

        Returns:
            None: This method updates the wall state in place.
        """
        if self.north:
            self.north = False
        else:
            raise WallError('The northern wall is already open')

    def _pop_south(self) -> None:
        """Remove the south wall of the cell.

        Returns:
            None: This method updates the wall state in place.
        """
        if self.south:
            self.south = False
        else:
            raise WallError('The southern wall is already open')

    def _pop_east(self) -> None:
        """Remove the east wall of the cell.

        Returns:
            None: This method updates the wall state in place.
        """
        if self.east:
            self.east = False
        else:
            raise WallError('The eastern wall is already open')

    def _pop_west(self) -> None:
        """Remove the west wall of the cell.

        Returns:
            None: This method updates the wall state in place.
        """
        if self.west:
            self.west = False
        else:
            raise WallError('The western wall is already open')

    def _create_north(self) -> None:
        """Create the north wall of the cell.

        Returns:
            None: This method updates the wall state in place.
        """
        if not self.north:
            self.north = True
        else:
            raise WallError('The northern wall already exists')

    def _create_south(self) -> None:
        """Create the south wall of the cell.

        Returns:
            None: This method updates the wall state in place.
        """
        if not self.south:
            self.south = True
        else:
            raise WallError('The southern wall already exists')

    def _create_east(self) -> None:
        """Create the east wall of the cell.

        Returns:
            None: This method updates the wall state in place.
        """
        if not self.east:
            self.east = True
        else:
            raise WallError('The eastern wall already exists')

    def _create_west(self) -> None:
        """Create the west wall of the cell.

        Returns:
            None: This method updates the wall state in place.
        """
        if not self.west:
            self.west = True
        else:
            raise WallError('The western wall already exists')
