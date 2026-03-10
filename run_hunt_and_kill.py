#!/usr/bin/env python3
import argparse

from generators import HuntAndKillGenerator


def render_ascii(maze) -> str:
    lines = []
    wid, leng = maze.wid, maze.leng

    top = "+"
    for x in range(leng):
        top += ("---" if maze.body[0][x].north else "   ") + "+"
    lines.append(top)

    for y in range(wid):
        middle = "|" if maze.body[y][0].west else " "
        for x in range(leng):
            if maze.body[y][x].is_ft:
                cell_text = "###"
            elif [x, y] == maze.entry:
                cell_text = " S "
            elif [x, y] == maze.out:
                cell_text = " E "
            else:
                cell_text = "   "
            middle += cell_text
            middle += "|" if maze.body[y][x].east else " "
        lines.append(middle)

        bottom = "+"
        for x in range(leng):
            bottom += ("---" if maze.body[y][x].south else "   ") + "+"
        lines.append(bottom)

    return "\n".join(lines)


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
        entry=[0, 0],
        out=[args.leng - 1, args.wid - 1],
        wid=args.wid,
        leng=args.leng,
    )
    generator.generate_maze(0, 0)
    print(render_ascii(generator.maze))


if __name__ == "__main__":
    main()
