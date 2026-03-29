import curses


def main(stdscr):
    curses.init_pair(5, curses.COLOR_BLACK, curses.COLOR_BLUE)
    stdscr.clear()
    stdscr.addstr(3, 15, "hello world", curses.color_pair(5))
    stdscr.refresh()
    stdscr.getch()


curses.wrapper(main)





























# def main(stdscr):
#     # 1. Clear the screen
#     stdscr.clear()

#     # 2. Add a character at row 10, column 20
#     # Syntax: stdscr.addstr(y, x, "text")
#     i = 0
#     while i <= 10:
#         stdscr.addstr(0, i, "█")
#         if i % 2 == 0:
#             stdscr.addstr(1, , "█")
#         stdscr.addstr(i, 0, "█")
#         i = i + 1

#     # 3. Refresh to show the changes
#     stdscr.refresh()

#     # 4. Wait for a key press so the program doesn't close instantly
#     stdscr.getch()

# # The wrapper handles the setup and cleanup safely


# curses.wrapper(main)


# screen = curses.initscr()
# curses.noecho()
# curses.cbreak()
# screen.getch()
# secreeeen = None
# secreeeen = curses.wrapper()
# secreeeen.refresh()
# secreeeen.getch()
# screen.refresh()
