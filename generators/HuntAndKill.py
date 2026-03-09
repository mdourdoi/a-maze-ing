from source import MazeGenerator, Maze
from random import choice


class HuntAndKillGenerator(MazeGenerator):

    def __init__(self, name: str):
        super().__init__(name)

    def __init__(self,
                 name: str,
                 entry: List[int, int],
                 out: List[int, int],
                 wid: int,
                 leng: int):
        super().__init__(name, entry, out, wid, leng)

    def generate_maze(self, x: int, y: int) -> Maze:
