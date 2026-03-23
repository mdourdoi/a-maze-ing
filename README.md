*This project has been created as part of the 42 curriculum by <login1>[, <login2>[, <login3>[...]]].*

---

# 🧩 A-MAZE-ING

![Python](https://img.shields.io/badge/Python-3.x-blue)
![Status](https://img.shields.io/badge/Status-Completed-success)
![42](https://img.shields.io/badge/School-42-black)

## 📖 Description

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

### 🧠 TABLE OF CONTENT:
- Instructions
- Configuration
- Maze Generation Algorithm
- Maze Solver Algorithm
- Graphical Display
- Output File

---

## ⚙️ Instructions

### 📦 Installation

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

## ⚙️ CONFIGURATION

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

## ⚙️ MAZE GENERATION ALGORITHM

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
> and expand from it. This strategy works with 2 list of cells

### Openning map

> Destroy max 20% of the map randomely, but it can be modified whitin the code

>## ⚙️ OUTPUT FILE
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