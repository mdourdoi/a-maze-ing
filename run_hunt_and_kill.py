#!/usr/bin/env python3
import argparse
from mlx import Mlx
from typing import Any, List
from source import MazeCell
from generators import HuntAndKillGenerator


def main() -> None:
    parser = argparse.ArgumentParser(
        description="Generate and print a maze with Hunt-and-Kill."
    )
    parser.add_argument(
        "--wid",
        type=int,
        default=10,
        help="Number of rows (y).")
    parser.add_argument(
        "--leng", type=int, default=20, help="Number of columns (x)."
    )
    parser.add_argument("--seed", type=int, default=None)
    args = parser.parse_args()

    m = Mlx()
    mlx = m.mlx_init()
    win = m.mlx_new_window(mlx, 1200 + 1, 800 + 1, 'Maze renderer')

    menu_items = ["Prim's algorithm", 'Hunt and kill', 'Quit']
    selected = 0
    blink_on = True
    generator = None
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

    def draw_cell(
            pos: List[int],
            cell: MazeCell) -> None:

        nonlocal cell_size_x, cell_size_y
        nonlocal h_wall, v_wall, bg_image, start_image, end_image, ft_image

        cell_pos_x = pos[0] * cell_size_x
        cell_pos_y = pos[1] * cell_size_y

        if cell.is_ft:
            m.mlx_put_image_to_window(
                mlx, win, ft_image, cell_pos_x, cell_pos_y)
            m.mlx_put_image_to_window(mlx, win, h_wall, cell_pos_x, cell_pos_y)
            m.mlx_put_image_to_window(
                mlx, win, h_wall, cell_pos_x, cell_pos_y + cell_size_y)
            m.mlx_put_image_to_window(mlx, win, v_wall, cell_pos_x, cell_pos_y)
            m.mlx_put_image_to_window(
                mlx, win, v_wall, cell_pos_x + cell_size_x, cell_pos_y)
            return

        m.mlx_put_image_to_window(mlx, win, bg_image, cell_pos_x, cell_pos_y)

        if cell.is_start:
            m.mlx_put_image_to_window(
                mlx, win, start_image, cell_pos_x, cell_pos_y)

        if cell.is_end:
            m.mlx_put_image_to_window(
                mlx, win, end_image, cell_pos_x, cell_pos_y)

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

    def on_key(key: int, ctx: Any) -> None:

        nonlocal started, generator, iterator, selected, mode_selected
        nonlocal cell_size_x, cell_size_y, v_wall, h_wall, bg_image
        nonlocal start_image, end_image, ft_image

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
            started = True
            mode_selected = menu_items[selected]
            m.mlx_clear_window(mlx, win)
            m.mlx_destroy_image(mlx, img)

            # Exit if 'Quit' is selected
            if mode_selected == 'Quit':
                m.mlx_loop_exit(mlx)
                return

            print('Selected:', mode_selected)
            if mode_selected == 'Hunt and kill':
                generator = HuntAndKillGenerator(
                    name="hunt-and-kill",
                    entry=[39, 7],
                    out=[4, 19],
                    wid=args.wid,
                    leng=args.leng,
                    seed=args.seed
                )
            cell_size_x = 1200 // generator.leng
            cell_size_y = 800 // generator.wid
            h_wall = make_solid_image(cell_size_x, 1, 0xFFFF0000)
            v_wall = make_solid_image(1, cell_size_y, 0xFFFF0000)
            bg_image = make_solid_image(cell_size_x, cell_size_y, 0xFF000000)
            start_image = make_solid_image(
                cell_size_x, cell_size_y, 0xFF008000)
            end_image = make_solid_image(cell_size_x, cell_size_y, 0xFF0000FF)
            ft_image = make_solid_image(cell_size_x, cell_size_y, 0xFFFFFFFF)
            iterator = generator.generate_maze()
            for j in range(generator.wid):
                for i in range(generator.leng):
                    if (generator.maze.body[j][i].is_ft or
                        generator.maze.body[j][i].is_start or
                            generator.maze.body[j][i].is_end):
                        draw_cell([i, j], generator.maze.body[j][i])

    def on_loop(ctx: Any) -> None:
        nonlocal started, iterator, frame, blink_on

        if mode_selected is None:
            frame += 1
            if frame % 10 == 0:
                blink_on = not blink_on
                render_menu()
                return

        if mode_selected == 'Hunt and kill':
            try:
                for _ in range(3):
                    iteration = next(iterator)
                    x = iteration[0]
                    y = iteration[1]
                    draw_cell([x, y], generator.maze.body[y][x])
                    direction = iteration[2]
                    if direction == 'north':
                        draw_cell([x, y - 1], generator.maze.body[y - 1][x])
                    if direction == 'south':
                        draw_cell([x, y + 1], generator.maze.body[y + 1][x])
                    if direction == 'east':
                        draw_cell([x + 1, y], generator.maze.body[y][x + 1])
                    if direction == 'west':
                        draw_cell([x - 1, y], generator.maze.body[y][x - 1])
            except StopIteration:
                started = False
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
    m.mlx_loop_exit(mlx)
    m.mlx_destroy_window(mlx, win)
    m.mlx_release(mlx)


if __name__ == "__main__":
    main()
