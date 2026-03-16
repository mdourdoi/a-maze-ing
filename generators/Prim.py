from source import MazeGenerator
from typing import List, Generator
import random


class PrimGenerator(MazeGenerator):

    def __init__(self,
                 name: str,
                 entry: List[int],
                 out: List[int],
                 height: int,
                 wid: int,
                 seef: int | None = None):
        super().__init__(name, entry, out, height, wid, seef)

    def generate_maze(self) -> Generator:
        cur_x, cur_y = self.maze.entry[0], self.maze.entry[1]
        self.maze.body[cur_y][cur_x].visit()
        frontier: set = {}
        neighbours = self.maze.get_valid_neighbours(cur_x, cur_y)
        frontier += {(v[0], v[1]) for v in neighbours.values()}
        while frontier:
            frontier_cell = random.choice(frontier)
            self.maze.body[frontier_cell[0]][frontier_cell[1]].visit()
            direction = random.choice(
                self.maze.get_visited_neighbours(frontier_cell[0],
                                                 frontier_cell[1]))
            self.maze.body.carve(frontier_cell[0],
                                 frontier_cell[1],
                                 direction.key())
            neighbours = self.maze.get_valid_neighbours(frontier_cell[0],
                                                        frontier_cell[1])
            frontier = (frontier + {(v[0], v[1]) for v in neighbours.values()}) - frontier_cell
            yield [frontier_cell[0], frontier_cell[1], direction.key()]
