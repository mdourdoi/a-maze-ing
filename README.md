*This project has been created as part of the 42 curriculum by <login1>[, <login2>[, <login3>[...]]].*

---

# A-MAZE-ING

![Python](https://img.shields.io/badge/Python-3.x-blue)
![Status](https://img.shields.io/badge/Status-Completed-success)
![42](https://img.shields.io/badge/School-42-black)

## Description

>
> A-Maze-Ing is a Python3 project that combine Maze Generation, Maze Solving algorithms and 
> Graphical Display.
>
> The purpose of this project is to **easily generate** multiple **maps** that can
> be used for different **Game projects** 
> The Graphical User Interface(GUI) is made by using the **MiniLibX graphical library** given by
> 42School
>
> In Addition to that, the project offers a fully usable **Maze Generator package** in Python that can
> be integrate in any project
>

### TABLE OF CONTENT:
- Instructions
- Project
- Configuration
- Maze Generation Algorithm
- Maze Solver Algorithm
- Graphical Display
- Output File

---

## Instructions

### Installation

```bash
# Clone the repository
git clone <repo_url>

# Navigate into the project
cd A-MAZE-ING

# Compiling and installing 
make
```

### Runnig

```bash
python3 a_maze_ing.py config.txt
```
## Project

## CONFIGURATION

### CONFIG FILE

>
>   Maze Generation parameters can be modified passing by the file ' *config.txt* '
>
>   This config file work by using 'KEY=VALUE' pair per line.
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
>   SEED=42 
>   ```
>   **Config Key value:**
>
>   -   **WIDTH** :
> 
>       Give the width of Maze
>   -   **HEIGHT** :
> 
>       Give the height of Maze
>   -   **ENTRY** :
> 
>       Give the coordonate of the Maze
>       entry must be "y,x" 
>       where y and x are integers
>   -    **EXIT** :
> 
>       Give the coordonate of the Maze
>       exit, the value must be "y,x" 
>       where y and x are integers
>   -    **OUTPUT_FILE** :
> 
>       Specify the name of the outfile where are contains the data of the Generated Maze and the 
>       shortest path from entry to solution
>   -    **PERFECT** :
>
>       Boolean('True'/'False') value that specify if the Maze must be a **perfect maze** (only one path from the entry and the exit) or an **imperfect maze** (open maze with multiple path from entry to exit)
>   -    **SEED** :
>
>       Specify a seed value to generate the Maze, different seed will generate different maze,
>       keeping the same seed will result to generate the same Maze

## MAZE GENERATION ALGORITHM

### Prelude:

>
> The **A-Maze-Ing** package contain 2 maze generation Algorithm. The **HuntAndKill** Algorithm and **Prim** Algorithm.
> Number of algorithm can be **easily increased** by adding new generator object, as long as it respect the structure
> of the **MazeGenerator Class** and yield every step of the generation correctly and return a Python Generator that contains
> every position and direction of the algorithm.
> 

### Hunt And Kill

> The Hunt And Kill algorithm is a simple algorithm that create long winding paths by simply searching the least advanced 
> unvisited cell (left to right, up to down) that is connected to the maze and start to carve a path until it has no unvisited
> cells. Repeat until there is not unvisited cell within the maze. This method unsure that the generated maze will be perfect.
>
> #### Pseudo Code:
>
> ```
>   HuntAndKill(start_location):
>       while map_has_unvisited_cell:
>           build_path:
>               /* First path to create at start position */
>               while valid_neighbour(location):
>                   neighbor = choose random neighbor
>                   carve_to_neighbor
>                   location = neighbor
>           Look_for_unvisited_cell:
>               /* Iterate through the grid to look for  */
>               for y_cell in maze:
>                   for x_cell in maze:
>                       if x_cell is unvisited:
>                           return x_cell as new_position       
> ```

### Prim

> The Prim algorithm is much different from the Hunt And Kill, it begin from an arbitery cell
> and expand from it. This strategy works with a list of unvisited cells, the frontier, that
> contains all unvisited cell neighboring the maze. The algorithm will choose randomly one Cell
> of the frontier, carve a path to the maze from it and remove the cell from the frontier, 
> repeat until there is no cell in frontier. 
>
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
### Openning map

> The opening map algorithm is used to pass from a Perfect maze to an Imperfect. 
> The algorithm is pretty straightforward, it try to destroy a wall randomly if 
> the conditions are respected (Not creating corridors larger than 2 cells).

## Maze Solver Algorithm

### Prelude:
> 
> The project contains one solver algorithm and can't add anymore easily due to some
> Architectural Constraint. The solving Algorithm is link to the MazeGenerator Class
> it start automatically when the maze is generated.

### A* Algorithm:

> The A* Algorithm is used as a solving algorithm, because of his performance. It is 
> an alternative to Dijkstra Algorithm which is used for graph exploration and pathfinding.
> The main difference from Dijkstra is the use of an heuristic function h(n), the estimated 
> distance from node n and the goal, and the use of g(n), the distance from the node n to the 
> starting point. 
>
> The heuristic function h behave as a criteria to get the shortest path to the goal. Two type
> of heuristic function are traditionaly use, the euclidian heuristic, which calculate the  
> straight distance between 2 point and the Manhattan geometry which calculate the distance 
> by doing the sum of the absolute difference of their respective Cartesian coordinates.
>
> The value of each node is calculated by making the sum f of the g(n) and h(n) functions.
> At each step the algorithm picks a neighbor Cell and calculate the score f of that one,
> if the cost of that node is inferior of the one corresponding node in the came_from list
> it while replace it. This steps repeat until it find the Exit Cell or until there is no Cells
> in the open list anymore. This method unsure us to find the shortest path from the start to 
> the exit.
>
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

>## OUTPUT FILE
>    **output file format:**
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