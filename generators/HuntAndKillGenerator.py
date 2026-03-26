from source import MazeGenerator
from typing import List, Generator


class HuntAndKillGenerator(MazeGenerator):
    """Maze generator based on the Hunt-and-Kill algorithm."""

    def __init__(self,
                 name: str,
                 entry: List[int],
                 out: List[int],
                 height: int,
                 wid: int,
                 seed: int | None = None):
        """Initialize a Hunt-and-Kill maze generator.

        Args:
            name: Human-readable name of the generator.
            entry: Entry cell coordinates as [x, y].
            out: Exit cell coordinates as [x, y].
            height: Maze height in number of cells.
            wid: Maze width in number of cells.
            seed: Optional seed used for deterministic randomness.

        Returns:
            None: This constructor initializes the instance in place.
        """
        super().__init__(name, entry, out, height, wid, seed)

    def _generate_maze(self) -> Generator[List[int], None, None]:
        """Generate the maze using the Hunt-and-Kill strategy.

        Returns:
            Generator[List[int], None, None]: A generator yielding the
            coordinates of each newly visited cell.
        """
        cur_x, cur_y = self.maze.entry[0], self.maze.entry[1]
        self.maze.body[cur_y][cur_x]._visit()
        running = True
        self.maze.body[cur_y][cur_x]._visit()
        while running:
            valid_neighbours = self.maze._get_valid_neighbours(cur_x, cur_y)
            if valid_neighbours:
                next_dir = self._random.choice(list(valid_neighbours.keys()))
                self._carve(cur_x, cur_y, next_dir)
                chosen = valid_neighbours[next_dir]
                cur_x, cur_y = chosen[0], chosen[1]
                self.maze.body[cur_y][cur_x]._visit()
                yield [cur_x, cur_y]
            else:
                running = False
                for j in range(self.height):
                    for i in range(self.wid):
                        if (not self.maze.body[j][i]._is_visited
                                and not self.maze.body[j][i]._is_ft):
                            vis_neigh = self.maze._get_visited_neighbours(i, j)
                            if vis_neigh:
                                running = True
                                next_dir = self._random.choice(
                                    list(vis_neigh.keys()))
                                self._carve(i, j, next_dir)
                                cur_x, cur_y = i, j
                                self.maze.body[cur_y][cur_x]._visit()
                                yield [cur_x, cur_y]
                        if running is True:
                            break
                    if running is True:
                        break
        self.is_generated = True
