*This project has been created as part of the 42 curriculum by melschmi and mdourdoi*

---

# A-MAZE-ING

![Python](https://img.shields.io/badge/Python-3.10-blue)
![Status](https://img.shields.io/badge/Status-Completed-success)
![42](https://img.shields.io/badge/School-42-black)

# Table of contents:
- Description
- Instructions
- Project
  - Maze generation algorithms
  - Maze solver algorithm
- Output file
- Graphical user interface
- Reusability and package
- Team and project management

# Description


A-Maze-Ing is a Python3 project that combine maze generation, maze solving algorithms and graphical display.

The purpose of this project is to **easily generate** multiple **mazes** that can be reused for different **game projects** 

The Graphical User Interface (GUI) is made by using the **MiniLibX graphical library** given by 42School.

In addition to that, the project offers two fully usable **maze generators: HuntAndKillGenerator and PrimGenerator** in Python that canbe integrated in any project. 


# Instructions

### Installation

```bash
# Clone the repository
git clone <repo_url>

# Navigate into the project
cd a-maze-ing

# Compiling and installing 
make install
```

### Running

DISCLAIMER : You need to have the mlx package installed (at least version 2.2). A wheel is available in the ressources folder.

```bash
python3 a_maze_ing.py config.txt
```

or

```bash
make run
```
# Resources

- To get the global idea of each algorithms : https://professor-l.github.io/mazes/ and https://weblog.jamisbuck.org/2011/2/7/maze-generation-algorithm-recap

- AI was used as a helper to understand how the MLX works and as a way to be faster for documentation (for example what is the value of each key for the key_hook of the MLX or how create an instance of random with a seed). It was also used in the early stages for early stage development to represent a maze on the terminal, this wasn't kept in the final project.

# Project

## Maze generation algorithms

### Prelude

The **a-maze-ing** package contains 2 maze generation algorithm : the **HuntAndKill** algorithm and **Prim's** algorithm. Each corresponds to a generator that can be instanciated.

New generators can be created via the abstract class **MazeGenerator**, only the method **generate_maze** must be implemented as the solver is within the abstract class. The method must work accordingly to the others already implemented : visited cells must be marked as visited, and it must instanciate a Generator that yields a list [x, y] where x and y are the coordinates of the cell you're trying to update (the MLX will update all cells around this one).

We decided to go with these algorithm because they naturally create perfect mazes, and we decided to go for the "make a perfect maze then break walls" plan for imperfect algorithms because it seemed easier.
 
### Hunt And Kill

The Hunt And Kill algorithm is a simple algorithm : starting from the entry of the maze, you do a random walk as long as you have unvisited neighbours. When you end up in a cell with no unvisited neighbours, you search the first unvisited cell (left to right, top to bottom) with at least one or more visited neighbour(s), you join it to a visited neighbour (randomly if more than one) then do a random walk again and repeat this process until the maze has no unvisited cells. This ensures a perfect maze.

> #### Pseudo Code:
>
> ```
>   HuntAndKill(start_location):
>       current_location = start_location
>       while map_has_unvisited_cell:
>           build_path:
>               while valid_neighbour(current_location):
>                   neighbour = random valid neighbour from current_location
>                   carve_to_neighbor
>                   current_location = neighbour
>               if current_location has no valid neighbour:
>                   for y in maze height:
>                       for x in maze width :
>                           if maze(x, y) is unvisited and maze(x, y) has a visited neighbour:
>                               current_location = maze(x, y)
> ```

### Prim

The Prim's algorithm is much different from the Hunt And Kill, it begins from an arbitrary cell and expands from it (we decided to choose the entry). This strategy works with a list of unvisited cell(s), the frontier, that contains all unvisited cells neighboring in the maze. The algorithm will choose one random cell in the frontier, carve a path from the maze to it and remove the cell from the frontier, then update the frontier. Repeat until the frontier is empty. This algorithm also ensures a perfect maze.

> #### Pseudo Code:
>
> ```
>   Prim(start_cell):
>       frontier = get_valid_neighbours(start_cell)
>       while frontier:
>            new_pos = choose_random_cell(frontier)
>            frontier += get_valid_neighbours(new_pos)
>            carve_to_maze(new_position)
>            frontier.remove(new_position)
> ```
>
### Create imperfect mazes

Since all our algorithms create perfect mazes, we added a way to break several walls (max 20% of the maze) to render an imperfect maze instead of implementing an algorithm to create imperfect ones. This is the _make_imperfect method in MazeGenerator.

Of course, before breaking a wall in this step, we always check if this would create a 3x3 pattern which is forbidden by the subject.

# Maze Solver Algorithm

### Prelude

The project contains one solver algorithm within the MazeGenerator abstract class. We made the choice to implement just one since the main focus is to generate mazes, not solving them.

### A* Algorithm:

We choose A* algorithm as a solving algorithm because of its performance. It is an alternative to the Dijkstra's algorithm which is used for graph exploration and pathfinding.

The main difference comparing to Dijkstra is the use of an heuristic function h(n), the estimated distance from node n and the goal, and the use of g(n), the distance from the node n to the starting point. 

The heuristic function h behaves as a criteria to get the shortest path to the goal. Two types of heuristic functions are traditionaly used, the euclidian heuristic, which calculate the straight distance between 2 point and the Manhattan geometry which calculate the distance by doing the sum of the absolute difference of their respective Cartesian coordinates.

The value of each node is calculated by making the sum f of the g(n) and h(n) functions. At each step the algorithm picks a neighbor cell and calculates its score f, if the cost of that node is inferior to the corresponding node in the came_from list it replaces it. This steps repeats until it finds the exit cell or until there is no cell in the open list anymore. This method ensures us to find the shortest path from the start to the exit.

> #### Pseudo Code:
>```
>   a_star(start_position):
>       open_list = [start_position]
>       came_from = {}
>       g_score{start_position: 0}
>       f_score{start_position: h(start_position)}
>       while open_list is not empty:
>           current_pos = min_f_score_position
>           if current_pos == exit:
>               return reverse(came_from)
>           for neighbor(current_position):
>               if neighbor < came_from[neighbor]:
>                   update came_from[neighbor] = current_pos
>```

# Output file
The output file generated by the program contains the data that represents the maze, the entry and the exit coordonates of the maze, and the shortest solution path from start to exit. 

>    **Output file format:**
>    ```
>       91393D1117
>       8428050407
>       AF802FEF87
>       AFEE817F87
>       AFFFAEFFC3
>       813FAFD516
>       842BABFF87
>       A940001107
>       80382EC007
>       EC6C47D6C7
>
>       0,0
>       9,9
>       SSSSSSEESEEEESEESE
>    ```
>
The first block of data is the hexadecimal value of each cell, the value symbolizes the open wall(s) of the cells described by the subject.

The two next lines are the entry and exit coordinates.

The last line is the solution path, each instruction is the direction to take starting from the entry:

>   -   N: North
>   -   S: South
>   -   E: East
>   -   W: West

# Graphic user interface

### Description
We used the MLX to implement a visual representation of the maze.

We first render a simple menu asking the user to select one of the 2 available algorithms (up and down + enter to select) and then create one in real time using the loop hook from the MLX (with big mazes it can take a while to generate). This gives an interactive way of representing the approaches we had to generate mazes.

When a maze is fully rendered, you have several inputs to interact with it : regenerate a maze with a specific algorithm, solve it, export the file, change colors, etc ... The maze must be fully rendered before these inputs to avoid incoherent behavior like solving before the end, or graphical bugs (you can still press Esc or the cross button to exit whenever you want). Additionaly, the maze must be solved before exporting.

The parameters used for the generation are the ones in the config file explained below.

### Config file


For the graphical display, maze generation parameters can be modified passing by the file '**config.txt**'. A valid example of a config file is available in the repository.

>   This config file works by using 'KEY=VALUE' pair per line.
>
>   **Attended Config file Format :**
>
>  ```
>   WIDTH=80
>   HEIGHT=80
>   ENTRY=0,0
>   EXIT=42,75 
>   OUTPUT_FILE=maze.txt
>   PERFECT=False
>   ```
>   **Config Key value:**
>
>   -    **WIDTH**
> 
>       Gives the width of maze.
>   -    **HEIGHT**
> 
>       Gives the height of maze.
>
>   -    **ENTRY**
>
>       Gives the coordonate of the maze's entry, the value must be "x,y" where x and y are integers.
>   -    **EXIT**
> 
>       Gives the coordonate of the maze's exit, the value must be "x,y" where x and y are integers.
>   -    **OUTPUT_FILE**
> 
>       Specifies the name of the outfile where are contains the data of the Generated Maze and the shortest path from entry to solution.
>   -    **PERFECT**
>
>       Boolean ('True'/'False') value that specifies if the Maze must be a perfect maze (only one path from the entry and the exit) or an imperfect maze (open maze with multiple paths from entry to exit).
>
>   -    **OPTIONAL : SEED**
>
>       Specifies a seed value to generate the maze, a different seed will generate a different maze, keeping the same seed will result in generating the same maze when using the same algorithm. It needs an integer value, or 'None'. If set at 'None', it will behave as if the line is not in the file.

### Misc about the GUI

- Instead of drawing each pixel when we need to render something, we create static images that get destroyed after each use.
- When the config file contains a seed that is not 'None', a warning message is displayed when generating a maze to inform the user that each algorithm will generate the same maze when reloading.
- When generating the maze, we always redraw all the neighbouring cells to prevent visual anomalies sinc a wall is shared with its neighbours, and its angles with all the surrouding cells. It also allows us to just draw around a cell without having to look at which cell it carves to.

# Reusability and package

This whole project was also made to be used outside of the visual interface, so it is possible to import it as a package and reuse the different classes alone.

Since we need a lot of things for the display and not all of them can be used as they are, it is highly **NOT** recommended to use the methods starting with an underscord without knowing how all this project works. Lots of attributes are open in case you want to tweak the maze, you can modify it at your own risk.

The arguments to pass to instanciate an instance of a generator are self explanatory, you just need to create an instance of your choosen generator (PrimGenerator or HuntAndKillGenerator) and pass the arguments.

Here is a list of what can be safely used and how it works :

### Attributes

- Cell :
	- north, south, east and west : boolean, True if there is a wall at this position
	- is_start, is_end : boolean, self explanatory

- Maze :
	- wid : strictly positive integer, the numbers of columns
	- height : strictly prositive integerthe number of rows
	- body : List[List[MazeCell]] representing a maze, thus the cell at the coordinates [x, y] is self.body[y][x]
	- entry, out : List[int], positions of entry and exit

- MazeGenerator (PrimGenerator and HuntAndKillGenerator) :
	- name : str, name of the generator (in case you need to streamline creation and differentiate several generators)
	- maze : Maze, the maze that will be modified by the generator
	- is_solved, is_generated : bool, self explanatory
	- seed : int or None, the seed for the random generation
	- solution : List[tuple(int, int)], the sequence of coordinates for the shortest solution
	- some attributes are the same as the maze's for easy access without long lines : entry, out, height, wid

### Methods

- Maze :
	- is_top_border, is_bot_border: boolean, self explanatory, takes the row number of a cell as an argument
	- is_left_border, is_right_border: boolean, self explanatory, takes the column number of a cell as an argument

- MazeGenerator (PrimGenerator and HuntAndKillGenerator) :
	- reset_maze: resets the maze within the generator
	- create_full_maze(filename: str, perfect: bool, export: bool = False):
		- standalone method to do what the visual interface does
		- generates the maze inside the generator if it's not already generated and makes it imperfect if perfect = False
		- solves it if it's not already solved
		- if export = True, it exports the maze inside the generator in a file named *filename*
		- before creating a new maze, you should call reset_maze before, or it will just do nothing
	- basic_example : instanciate a generator with a 20x15 imperfect maze and no seed, the entry is at [0,0] and the exit is at [19,14]


# Team and project management

## Roles

mdourdoi : 
 - Global structure idea
 - Creating basic classes
 - Hunt and kill algorithm
 - Visual interface implementation and managing the MLX
 - Global tweaking to transform the project into a reusable package
 - spongebob meme

melschmi :
 - Global structure improvements
 - Prim's algorithm
 - Solving algorithm
 - Output file
 - Makefile + packaging

Both :
 - README.md
 - Visual interface ideas

## How we planned versus reality

How we planned the project : A class for the cells, a class for the maze and a maze generator to act on the maze. The idea was to use cell and maze to get informations (mostly about the position of the cell and the state of it surrounding and itself) and the generator to perform actions on said maze and solve it.

The global plan was in this order : implementing classes -> implementing the specific algorithm to create valid mazes -> put the 42 logo in the middle -> render it using MLX -> improving the UI/UX -> doing the final chores (readme, makefile, mypy, etc ...)

It turned out to be the way to go, the only minor change we did was to transform generate_maze from a simple method into a Generator that acts then yield the position to update visually.

## What worked well

Globally everything in this project was straight forward except the MLX tantrums

## What could be improved

The MLX is quite slow when generating mazes and sometimes generates visual abnormalities like putting wrong images, it would have been better to use another library with less bugs.

## Specific tools

Outside of AI as a helper to go faster in our searches, we didn't use any specific tools.