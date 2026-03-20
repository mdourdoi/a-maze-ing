from helpers import get_config
from mlx import Mlx
from typing import Any, List, Generator
from source import MazeCell, Maze, MazeGenerator
from generators import HuntAndKillGenerator, PrimGenerator
import sys


def main() -> None:

    maze_width = 1200
    maze_height = 800
    side_panel_width = 360
    window_width = maze_width + side_panel_width
    window_height = maze_height
    panel_x = maze_width + 24
    command_hints = [
        'ENTER - Search/Hide shortest path',
        'H - Reload with Hunt And Kill',
        "P - Reload with Prim's algorithm",
        'W - Rotate wall colors',
        'F - Rotate 42 colors',
        'O - Create output file',
        'Esc - Quit']
    colors_rotation = [
        0xFFFFFFFF,
        0xFF0000FF,
        0xFFFF0000,
        0xFF008000,
        0xFFFFFF00]

    config_file = sys.argv
    if len(config_file) != 2:
        print('Invalid arguments. ', end='')
        print('Please input only the name of the config file')
        return
    try:
        config = get_config('config.txt')
        Maze(
            config['HEIGHT'],
            config['WIDTH'],
            config['ENTRY'],
            config['EXIT'])
        if 'SEED' in config.keys() and config['SEED'] is not None:
            command_hints.append('')
            command_hints.append('')
            command_hints.append('Warning: You used a seed.')
            command_hints.append('')
            command_hints.append('Reloading with')
            command_hints.append('the same algorithm will')
            command_hints.append('give you the same maze.')
    except Exception as cur_error:
        print(f"Error with given arguments: {cur_error}")
        return

    m = Mlx()
    mlx = m.mlx_init()
    win = m.mlx_new_window(
        mlx, window_width + 1, window_height + 1, 'Maze renderer')

    menu_items = ["Prim's algorithm", 'Hunt and kill', 'Quit']
    selected = 0
    blink_on = True
    generator: MazeGenerator | None = None
    imperfector: Generator | None = None
    frame = 0
    iterator: Generator | None = None
    generated = False
    solver: Generator | None = None
    solving = False
    solved = False
    show_solution = False
    mode_selected = None
    started = False
    spongebob_path = './assets/spongebob.png'
    img, w, h = m.mlx_png_file_to_image(mlx, spongebob_path)
    cell_size_x = None
    cell_size_y = None
    h_wall = None
    v_wall = None
    bg_image = None
    solving_img = None
    solved_img = None
    start_image = None
    end_image = None
    ft_image = None
    wall_color_index = colors_rotation.index(0xFFFF0000)
    ft_color_index = colors_rotation.index(0xFFFFFFFF)

    def make_solid_image(w: int, h: int, color: int) -> Any:
        img = m.mlx_new_image(mlx, w, h)
        data, bpp, sl, _ = m.mlx_get_data_addr(img)
        byte_per_pixel = bpp // 8
        c = color.to_bytes(4, "little")
        for y in range(h):
            row = y * sl
            for x in range(w):
                off = row + x * byte_per_pixel
                data[off:off + 4] = c
        return img

    def destroy_runtime_images() -> None:
        nonlocal img

        destroy_maze_images()
        if img is not None:
            m.mlx_destroy_image(mlx, img)
            img = None

    def destroy_maze_images() -> None:
        nonlocal h_wall, v_wall, bg_image
        nonlocal start_image, end_image, ft_image, solving_img, solved_img

        if h_wall is not None:
            m.mlx_destroy_image(mlx, h_wall)
            h_wall = None
        if v_wall is not None:
            m.mlx_destroy_image(mlx, v_wall)
            v_wall = None
        if bg_image is not None:
            m.mlx_destroy_image(mlx, bg_image)
            bg_image = None
        if start_image is not None:
            m.mlx_destroy_image(mlx, start_image)
            start_image = None
        if end_image is not None:
            m.mlx_destroy_image(mlx, end_image)
            end_image = None
        if ft_image is not None:
            m.mlx_destroy_image(mlx, ft_image)
            ft_image = None
        if solving_img is not None:
            m.mlx_destroy_image(mlx, solving_img)
            solving_img = None
        if solved_img is not None:
            m.mlx_destroy_image(mlx, solved_img)
            solved_img = None

    def build_generator(algo_name: str) -> MazeGenerator | None:
        if algo_name == 'Hunt and kill':
            return HuntAndKillGenerator(
                name="hunt-and-kill",
                entry=config['ENTRY'],
                out=config['EXIT'],
                height=config['HEIGHT'],
                wid=config['WIDTH'],
                seed=config['SEED'] if 'SEED' in config else None
            )
        if algo_name == "Prim's algorithm":
            return PrimGenerator(
                name="Prim's algorithm",
                entry=config['ENTRY'],
                out=config['EXIT'],
                height=config['HEIGHT'],
                wid=config['WIDTH'],
                seed=config['SEED'] if 'SEED' in config else None
            )
        return None

    def rebuild_ft_image() -> None:
        nonlocal ft_image
        nonlocal cell_size_x, cell_size_y

        if cell_size_x is None or cell_size_y is None:
            return
        if ft_image is not None:
            m.mlx_destroy_image(mlx, ft_image)
        ft_image = make_solid_image(
            cell_size_x, cell_size_y, colors_rotation[ft_color_index])

    def rebuild_color_images() -> None:
        nonlocal h_wall, v_wall
        nonlocal cell_size_x, cell_size_y

        if cell_size_x is None or cell_size_y is None:
            return
        if h_wall is not None:
            m.mlx_destroy_image(mlx, h_wall)
        if v_wall is not None:
            m.mlx_destroy_image(mlx, v_wall)
        h_wall = make_solid_image(
            cell_size_x + 1, 1, colors_rotation[wall_color_index])
        v_wall = make_solid_image(
            1, cell_size_y + 1, colors_rotation[wall_color_index])
        rebuild_ft_image()

    def draw_cell(
            pos: List[int],
            cell: MazeCell,
            draw_background: bool = True) -> None:

        nonlocal cell_size_x, cell_size_y
        nonlocal h_wall, v_wall, bg_image, start_image, end_image, ft_image
        nonlocal solving_img, solved_img, show_solution

        cell_pos_x = pos[0] * cell_size_x
        cell_pos_y = pos[1] * cell_size_y

        if draw_background:
            if cell.is_ft:
                m.mlx_put_image_to_window(
                    mlx, win, ft_image, cell_pos_x, cell_pos_y)
            elif cell.is_start:
                m.mlx_put_image_to_window(
                    mlx, win, start_image, cell_pos_x, cell_pos_y)
            elif cell.is_end:
                m.mlx_put_image_to_window(
                    mlx, win, end_image, cell_pos_x, cell_pos_y)
            else:
                m.mlx_put_image_to_window(
                    mlx, win, bg_image, cell_pos_x, cell_pos_y)

            if cell.is_solved and show_solution:
                if cell.is_solution:
                    m.mlx_put_image_to_window(
                        mlx, win, solved_img, cell_pos_x, cell_pos_y)
                else:
                    m.mlx_put_image_to_window(
                        mlx, win, solving_img, cell_pos_x, cell_pos_y)

        if cell.north:
            m.mlx_put_image_to_window(mlx, win, h_wall, cell_pos_x, cell_pos_y)
        if cell.south:
            m.mlx_put_image_to_window(
                mlx, win, h_wall, cell_pos_x, cell_pos_y + cell_size_y)
        if cell.west:
            m.mlx_put_image_to_window(mlx, win, v_wall, cell_pos_x, cell_pos_y)
        if cell.east:
            m.mlx_put_image_to_window(
                mlx, win, v_wall, cell_pos_x + cell_size_x, cell_pos_y)

    def redraw_zone(x: int, y: int) -> None:
        cells = []
        for j in range(max(0, y - 1), min(generator.height, y + 2)):
            for i in range(max(0, x - 1), min(generator.wid, x + 2)):
                cell = generator.maze.body[j][i]
                if (cell.is_visited or cell.is_ft
                        or cell.is_start or cell.is_end):
                    cells.append((i, j))
        draw_cell([x, y], generator.maze.body[y][x])
        for i, j in cells:
            draw_cell([i, j], generator.maze.body[j][i])
        draw_cell([x, y], generator.maze.body[y][x], False)
        for i, j in cells:
            draw_cell([i, j], generator.maze.body[j][i], False)

    def redraw_maze() -> None:
        if generator is None:
            return
        for j in range(generator.height):
            for i in range(generator.wid):
                draw_cell([i, j], generator.maze.body[j][i])

    def redraw_ft() -> None:
        if generator is None:
            return
        for j in range(generator.height):
            for i in range(generator.wid):
                if generator.maze.body[j][i].is_ft:
                    draw_cell([i, j], generator.maze.body[j][i])

    def render_commands_panel() -> None:
        title_color = 0x00FFD166
        text_color = 0x00CCCCCC

        m.mlx_string_put(mlx, win, panel_x, 60, title_color, 'Commands')
        for index, label in enumerate(command_hints):
            y = 110 + index * 32
            m.mlx_string_put(mlx, win, panel_x, y, text_color, label)

    def load_maze(algo_name: str) -> None:
        nonlocal started, generator, iterator, mode_selected
        nonlocal cell_size_x, cell_size_y, bg_image
        nonlocal start_image, end_image, imperfector, solver
        nonlocal solving, solving_img, solved_img, generated, solved
        nonlocal show_solution

        mode_selected = algo_name
        generator = build_generator(algo_name)
        if generator is None:
            return
        started = True
        generated = False
        solving = False
        solved = False
        show_solution = False
        imperfector = None
        iterator = None
        solver = None

        destroy_maze_images()
        m.mlx_clear_window(mlx, win)
        render_commands_panel()
        cell_size_x = maze_width // generator.wid
        cell_size_y = maze_height // generator.height
        bg_image = make_solid_image(
            cell_size_x, cell_size_y, 0xFF000000)
        start_image = make_solid_image(
            cell_size_x, cell_size_y, 0xFF008000)
        end_image = make_solid_image(
            cell_size_x, cell_size_y, 0xFF0000FF)
        rebuild_color_images()
        iterator = generator.generate_maze()
        for j in range(generator.height):
            for i in range(generator.wid):
                if (generator.maze.body[j][i].is_ft or
                    generator.maze.body[j][i].is_start or
                        generator.maze.body[j][i].is_end):
                    draw_cell([i, j], generator.maze.body[j][i])
        if not config['PERFECT']:
            imperfector = generator.make_imperfect()
        solving_img = make_solid_image(
            cell_size_x, cell_size_y, 0x88FFFF00)
        solved_img = make_solid_image(
            cell_size_x, cell_size_y, 0xFF3B2077)
        solver = generator.solve()

    def on_key(key: int, ctx: Any) -> None:

        nonlocal started, generator, iterator, selected, mode_selected
        nonlocal cell_size_x, cell_size_y, v_wall, h_wall, bg_image
        nonlocal start_image, end_image, ft_image
        nonlocal imperfector, solver, solving, solving_img, solved_img
        nonlocal generated, wall_color_index, ft_color_index, solved
        nonlocal show_solution

        # Exit with Esc
        if key == 65307:
            m.mlx_loop_exit(mlx)

        if (key == 65293 and mode_selected and generated and not solving
                and not solved):
            show_solution = True
            solving = True
            print("Solving...")

        elif key == 65293 and solved and not solving:
            show_solution = not show_solution
            redraw_maze()

        if generated and not solving and (key == 104 or key == 72):
            load_maze('Hunt and kill')

        if generated and not solving and (key == 112 or key == 80):
            load_maze("Prim's algorithm")

        if generated and (key == 119 or key == 87):
            wall_color_index = (wall_color_index + 1) % len(colors_rotation)
            rebuild_color_images()
            redraw_maze()

        if generated and (key == 102 or key == 70):
            ft_color_index = (ft_color_index + 1) % len(colors_rotation)
            rebuild_ft_image()
            redraw_ft()

        if generated and solved and not solving and (key == 111 or key == 79):
            generator.output(config['OUTPUT_FILE'])
        elif (key == 111 or key == 79):
            print("You need to solve the maze before creating the output")

        # Menu selection
        if key == 65362 and not mode_selected:
            selected = (selected - 1) % len(menu_items)
            render_menu()

        if key == 65364 and not mode_selected:
            selected = (selected + 1) % len(menu_items)
            render_menu()

        if key == 65293 and not mode_selected:
            mode_selected = menu_items[selected]

            # Exit if 'Quit' is selected
            if mode_selected == 'Quit':
                m.mlx_loop_exit(mlx)
                return

            print('Selected:', mode_selected)
            load_maze(mode_selected)

    def on_loop(ctx: Any) -> None:
        nonlocal started, iterator, frame, blink_on
        nonlocal imperfector, generator, generated
        nonlocal solved, solving

        if mode_selected is None:
            frame += 1
            if frame % 10 == 0:
                blink_on = not blink_on
                render_menu()
                return

        elif mode_selected and not solving:
            try:
                iteration = next(iterator)
                x = iteration[0]
                y = iteration[1]
                redraw_zone(x, y)
            except StopIteration:
                if imperfector is None:
                    started = False
                else:
                    try:
                        iteration = next(imperfector)
                        x = iteration[0]
                        y = iteration[1]
                        redraw_zone(x, y)
                    except StopIteration:
                        ...
                generated = True

        elif generated and solving:
            try:
                iteration = next(solver)
                x = iteration[0]
                y = iteration[1]
                draw_cell([x, y], generator.maze.body[y][x])
            except StopIteration:
                solving = False
                if not solved:
                    solved = True
                    print('Solved !')

    def render_menu():
        m.mlx_clear_window(mlx, win)
        m.mlx_put_image_to_window(
            mlx,
            win,
            img,
            (window_width - w) // 2,
            (window_height - h - 200) // 2)
        for i, label in enumerate(menu_items):
            y = 600 + i * 40
            is_sel = (i == selected)

            # petit clignotement du curseur
            cursor = ">> " if (is_sel and blink_on) else "   "
            color = 0x00FF5555 if is_sel else 0x00CCCCCC
            text = f"{cursor}{label}"

            m.mlx_string_put(mlx, win, window_width * 3 // 7, y, color, text)

    def on_close(ctx: Any):
        m.mlx_loop_exit(mlx)

    # Launching MLX
    m.mlx_clear_window(mlx, win)
    m.mlx_key_hook(win, on_key, None)
    m.mlx_hook(win, 33, 0, on_close, None)
    m.mlx_loop_hook(mlx, on_loop, None)
    m.mlx_loop(mlx)
    destroy_runtime_images()
    m.mlx_loop_exit(mlx)
    m.mlx_destroy_window(mlx, win)
    m.mlx_release(mlx)


if __name__ == "__main__":
    main()
