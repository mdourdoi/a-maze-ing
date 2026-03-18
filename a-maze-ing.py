from helpers import get_config
from mlx import Mlx
from typing import Any, List
from source import MazeCell, Maze
from generators import HuntAndKillGenerator, PrimGenerator
import sys


def main() -> None:

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
    except Exception as cur_error:
        print(f"Error with given arguments: {cur_error}")
        return

    m = Mlx()
    mlx = m.mlx_init()
    win = m.mlx_new_window(mlx, 1200 + 1, 800 + 1, 'Maze renderer')

    menu_items = ["Prim's algorithm", 'Hunt and kill', 'Quit']
    selected = 0
    blink_on = True
    generator = None
    imperfector = None
    frame = 0
    iterator = None
    mode_selected = None
    started = False
    spongebob_path = './assets/spongebob.png'
    img, w, h = m.mlx_png_file_to_image(mlx, spongebob_path)
    cell_size_x = None
    cell_size_y = None
    h_wall = None
    v_wall = None
    bg_image = None
    start_image = None
    end_image = None
    ft_image = None

    def make_solid_image(w: int, h: int, color: int):
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
        nonlocal img, h_wall, v_wall, bg_image
        nonlocal start_image, end_image, ft_image

        if img is not None:
            m.mlx_destroy_image(mlx, img)
            img = None

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

    def draw_cell(
            pos: List[int],
            cell: MazeCell,
            draw_background: bool = True) -> None:

        nonlocal cell_size_x, cell_size_y
        nonlocal h_wall, v_wall, bg_image, start_image, end_image, ft_image

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

    def on_key(key: int, ctx: Any) -> None:

        nonlocal started, generator, iterator, selected, mode_selected
        nonlocal cell_size_x, cell_size_y, v_wall, h_wall, bg_image
        nonlocal start_image, end_image, ft_image
        nonlocal imperfector

        # Exit with Esc
        if key == 65307:
            m.mlx_loop_exit(mlx)

        # Menu selection
        if key == 65362 and not mode_selected:
            selected = (selected - 1) % len(menu_items)
            render_menu()

        if key == 65364 and not mode_selected:
            selected = (selected + 1) % len(menu_items)
            render_menu()

        if key == 65293 and not mode_selected:
            mode_selected = menu_items[selected]
            m.mlx_clear_window(mlx, win)

            # Exit if 'Quit' is selected
            if mode_selected == 'Quit':
                m.mlx_loop_exit(mlx)
                return

            print('Selected:', mode_selected)
            if mode_selected == 'Hunt and kill':
                started = True
                generator = HuntAndKillGenerator(
                    name="hunt-and-kill",
                    entry=config['ENTRY'],
                    out=config['EXIT'],
                    height=config['HEIGHT'],
                    wid=config['WIDTH'],
                    seed=config['SEED'] if 'SEED' in config else None
                )
            if mode_selected == "Prim's algorithm":
                started = True
                generator = PrimGenerator(
                    name="Prim's algorithm",
                    entry=config['ENTRY'],
                    out=config['EXIT'],
                    height=config['HEIGHT'],
                    wid=config['WIDTH'],
                    seed=config['SEED'] if 'SEED' in config else None
                )
            if started:
                cell_size_x = 1200 // generator.wid
                cell_size_y = 800 // generator.height
                h_wall = make_solid_image(cell_size_x + 1, 1, 0xFFFF0000)
                v_wall = make_solid_image(1, cell_size_y + 1, 0xFFFF0000)
                bg_image = make_solid_image(
                    cell_size_x, cell_size_y, 0xFF000000)
                start_image = make_solid_image(
                    cell_size_x, cell_size_y, 0xFF008000)
                end_image = make_solid_image(
                    cell_size_x, cell_size_y, 0xFF0000FF)
                ft_image = make_solid_image(
                    cell_size_x, cell_size_y, 0xFFFFFFFF)
                iterator = generator.generate_maze()
                for j in range(generator.height):
                    for i in range(generator.wid):
                        if (generator.maze.body[j][i].is_ft or
                            generator.maze.body[j][i].is_start or
                                generator.maze.body[j][i].is_end):
                            draw_cell([i, j], generator.maze.body[j][i])
                if not config['PERFECT']:
                    imperfector = generator.make_imperfect()

    def on_loop(ctx: Any) -> None:
        nonlocal started, iterator, frame, blink_on, imperfector, generator

        if mode_selected is None:
            frame += 1
            if frame % 10 == 0:
                blink_on = not blink_on
                render_menu()
                return

        else:
            try:
                for _ in range(40):
                    iteration = next(iterator)
                    x = iteration[0]
                    y = iteration[1]
                    direction = iteration[2]
                    redraw_zone(x, y)
                    if direction == 'north':
                        redraw_zone(x, y - 1)
                    if direction == 'south':
                        redraw_zone(x, y + 1)
                    if direction == 'east':
                        redraw_zone(x + 1, y)
                    if direction == 'west':
                        redraw_zone(x - 1, y)
            except StopIteration:
                if imperfector is None:
                    started = False
                else:
                    try:
                        for _ in range(40):
                            iteration = next(imperfector)
                            x = iteration[0]
                            y = iteration[1]
                            direction = iteration[2]
                            if direction == 'north':
                                redraw_zone(x, y - 1)
                            if direction == 'south':
                                redraw_zone(x, y + 1)
                            if direction == 'east':
                                redraw_zone(x + 1, y)
                            if direction == 'west':
                                redraw_zone(x - 1, y)
                    except StopIteration:
                        ...
            return

    def render_menu():
        m.mlx_clear_window(mlx, win)
        m.mlx_put_image_to_window(
            mlx, win, img, (1200 - w) // 2, (800 - h - 200) // 2)
        for i, label in enumerate(menu_items):
            y = 600 + i * 40
            is_sel = (i == selected)

            # petit clignotement du curseur
            cursor = ">> " if (is_sel and blink_on) else "   "
            color = 0x00FF5555 if is_sel else 0x00CCCCCC

            m.mlx_string_put(mlx, win, 500, y, color, f"{cursor}{label}")

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
