from source import MazeGenerator
from typing import List, Generator


class HuntAndKillGenerator(MazeGenerator):

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
        running = True
        self.maze.body[cur_y][cur_x].visit()
        while running:
            valid_neighbours = self.maze.get_valid_neighbours(cur_x, cur_y)
            if valid_neighbours:
                next_dir = self.random.choice(list(valid_neighbours.keys()))
                self.carve(cur_x, cur_y, next_dir)
                chosen = valid_neighbours[next_dir]
                cur_x, cur_y = chosen[0], chosen[1]
                self.maze.body[cur_y][cur_x].visit()
                yield [cur_x, cur_y]
            else:
                running = False
                for j in range(self.height):
                    for i in range(self.wid):
                        if (not self.maze.body[j][i].is_visited
                                and not self.maze.body[j][i].is_ft):
                            vis_neigh = self.maze.get_visited_neighbours(i, j)
                            if vis_neigh:
                                running = True
                                next_dir = self.random.choice(
                                    list(vis_neigh.keys()))
                                self.carve(i, j, next_dir)
                                cur_x, cur_y = i, j
                                self.maze.body[cur_y][cur_x].visit()
                                yield [cur_x, cur_y]
                        if running is True:
                            break
                    if running is True:
                        break
