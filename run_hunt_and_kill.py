#!/usr/bin/env python3
import argparse

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

    generator = HuntAndKillGenerator(
        name="hunt-and-kill",
        entry=[39, 7],
        out=[4, 19],
        wid=args.wid,
        leng=args.leng,
        seed=args.seed
    )
    # generator.generate_maze()
    # print(render_ascii(generator.maze))

    from mlx import Mlx
    from typing import Any, List
    from source import MazeCell

    m = Mlx()
    mlx = m.mlx_init()
    win = m.mlx_new_window(mlx, 2000 + 1, 1200 + 1, 'Maze renderer')

    def draw_cell(
            pos: List[int],
            maze_wid: int,
            maze_leng: int,
            cell: MazeCell) -> None:
        cell_size_x = 2000 // maze_leng
        cell_size_y = 1200 // maze_wid
        cell_pos_x = pos[0] * cell_size_x
        cell_pos_y = pos[1] * cell_size_y

        if cell.is_ft:
            for i in range(cell_size_x + 1):
                for j in range(cell_size_y + 1):
                    m.mlx_pixel_put(
                        mlx, win, cell_pos_x + i, cell_pos_y + j, 0xFFFFFFFF)
            for i in range(cell_size_x):
                m.mlx_pixel_put(
                    mlx,
                    win,
                    cell_pos_x + i,
                    cell_pos_y,
                    0xFFFF0000)
                m.mlx_pixel_put(
                    mlx,
                    win,
                    cell_pos_x +
                    i,
                    cell_pos_y +
                    cell_size_y,
                    0xFFFF0000)
            for j in range(cell_size_y):
                m.mlx_pixel_put(
                    mlx,
                    win,
                    cell_pos_x,
                    cell_pos_y + j,
                    0xFFFF0000)
                m.mlx_pixel_put(
                    mlx,
                    win,
                    cell_pos_x +
                    cell_size_x,
                    cell_pos_y +
                    j,
                    0xFFFF0000)
            return

        for i in range(cell_size_x):
            for j in range(cell_size_y):
                m.mlx_pixel_put(
                    mlx, win, cell_pos_x + i, cell_pos_y + j, 0xFF000000)

        if cell.is_start:
            for i in range(cell_size_x):
                for j in range(cell_size_y):
                    m.mlx_pixel_put(
                        mlx, win, cell_pos_x + i, cell_pos_y + j, 0xFF008000)

        if cell.is_end:
            for i in range(cell_size_x):
                for j in range(cell_size_y):
                    m.mlx_pixel_put(
                        mlx, win, cell_pos_x + i, cell_pos_y + j, 0xFF0000FF)

        if cell.north:
            for i in range(cell_size_x):
                m.mlx_pixel_put(
                    mlx,
                    win,
                    cell_pos_x + i,
                    cell_pos_y,
                    0xFFFF0000)
        if cell.south:
            for i in range(cell_size_x):
                m.mlx_pixel_put(
                    mlx,
                    win,
                    cell_pos_x +
                    i,
                    cell_pos_y +
                    cell_size_y,
                    0xFFFF0000)
        if cell.west:
            for j in range(cell_size_y):
                m.mlx_pixel_put(
                    mlx,
                    win,
                    cell_pos_x,
                    cell_pos_y + j,
                    0xFFFF0000)
        if cell.east:
            for j in range(cell_size_y):
                m.mlx_pixel_put(
                    mlx,
                    win,
                    cell_pos_x +
                    cell_size_x,
                    cell_pos_y +
                    j,
                    0xFFFF0000)

    def on_key(key: int, ctx: Any) -> None:
        nonlocal image_shown, started, iterator, generator
        if key == 65307:
            m.mlx_loop_exit(mlx)
        if key == 65293 and image_shown:
            image_shown = False
            m.mlx_clear_window(mlx, win)
            m.mlx_destroy_image(mlx, img)
        if key == 65293 and not image_shown and not started:
            started = True
            iterator = generator.generate_maze()
            for j in range(generator.wid):
                for i in range(generator.leng):
                    if (generator.maze.body[j][i].is_ft or
                        generator.maze.body[j][i].is_start or
                            generator.maze.body[j][i].is_end):
                        draw_cell([i, j], generator.wid, generator.leng,
                                  generator.maze.body[j][i])

    def on_loop(ctx: Any) -> None:
        nonlocal started, iterator
        if not started:
            return
        try:
            iteration = next(iterator)
            x = iteration[0]
            y = iteration[1]
            draw_cell([x, y], generator.wid, generator.leng,
                      generator.maze.body[y][x])
            direction = iteration[2]
            if direction == 'north':
                draw_cell([x, y - 1], generator.wid, generator.leng,
                          generator.maze.body[y - 1][x])
            if direction == 'south':
                draw_cell([x, y + 1], generator.wid, generator.leng,
                          generator.maze.body[y + 1][x])
            if direction == 'east':
                draw_cell([x + 1, y], generator.wid, generator.leng,
                          generator.maze.body[y][x + 1])
            if direction == 'west':
                draw_cell([x - 1, y], generator.wid, generator.leng,
                          generator.maze.body[y][x - 1])
        except StopIteration:
            started = False

    def on_close(ctx: Any):
        m.mlx_loop_exit(mlx)

    spongebob_path = './assets/spongebob.png'
    img, w, h = m.mlx_png_file_to_image(mlx, spongebob_path)
    m.mlx_clear_window(mlx, win)
    m.mlx_key_hook(win, on_key, None)
    m.mlx_hook(win, 33, 0, on_close, None)

    m.mlx_put_image_to_window(mlx, win, img, (2000 - w) // 2, (1200 - h) // 2)
    image_shown = True
    started = False
    iterator = None

    m.mlx_loop_hook(mlx, on_loop, None)
    m.mlx_loop(mlx)
    m.mlx_loop_exit(mlx)
    m.mlx_destroy_window(mlx, win)
    m.mlx_release(mlx)


if __name__ == "__main__":
    main()
