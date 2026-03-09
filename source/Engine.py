from MazeGenerator import MazeGenerator
from typing import Any


class MazeEngine:

    def __init__(self,
                 generator: MazeGenerator,
                 seed: Any):
        if not isinstance(generator, MazeGenerator):
            raise TypeError('Please input a valid maze generator')
        self.generator = generator
