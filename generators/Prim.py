from source import MazeGenerator
from typing import List, Generator


class PrimGenerator(MazeGenerator):

    def __init__(self,
                 name: str,
                 entry: List[int],
                 out: List[int],
                 height: int,
                 wid: int,
                 seed: int | None = None):
        super().__init__(name, entry, out, height, wid, seed)

    def generate_maze(self) -> Generator:
        cur_x, cur_y = self.maze.entry[0], self.maze.entry[1]
        self.maze.body[cur_y][cur_x].visit()
        frontier = {
            tuple(value) for value in list(
                self.maze.get_valid_neighbours(
                    cur_x, cur_y).values())}
        while frontier:
            x, y = self.random.choice(sorted(frontier))
            self.maze.body[y][x].visit()
            direction = self.random.choice(
                list(self.maze.get_visited_neighbours(x, y)))
            self.carve(x, y, direction)
            frontier.remove((x, y))
            new_frontier = {
                tuple(value) for value in list(
                    self.maze.get_valid_neighbours(
                        x, y).values())}
            frontier = frontier | new_frontier
            yield [x, y]
