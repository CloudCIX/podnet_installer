#!/usr/bin/python3
import curses
import os
import socket
import time
from configuration import validate_config
from hardware import validate_hardware
from software import validate_software
from utils import directory


class ScreenTooSmallError(Exception):
    """Raise when the screen is too small to display information properly """


# Setting up the Screen
# Create a screen
stdscr = curses.initscr()
# Allows use of Keyboard Control
stdscr.keypad(True)
# Hide the cursor
curses.curs_set(0)
# Initialise color
curses.start_color()
# Normal Text
curses.init_pair(1, curses.COLOR_BLACK, curses.COLOR_CYAN)
# Highlighted Text
curses.init_pair(2, curses.COLOR_WHITE, curses.COLOR_BLUE)
# Failed Verification
curses.init_pair(3, curses.COLOR_WHITE, curses.COLOR_RED)
# Passed Verification
curses.init_pair(4, curses.COLOR_BLACK, curses.COLOR_GREEN)
# Passed Verification
curses.init_pair(5, curses.COLOR_BLACK, curses.COLOR_YELLOW)
curses.init_pair(6, curses.COLOR_BLACK, curses.COLOR_BLUE)
curses.init_pair(7, curses.COLOR_BLACK, curses.COLOR_MAGENTA)
curses.init_pair(8, curses.COLOR_BLACK, curses.COLOR_WHITE)

# Standard Background
stdscr.bkgd(' ', curses.color_pair(1))

# Setting up Global Constants
# Size of window
rows, cols = stdscr.getmaxyx()
# Leave a black border
rows = rows - 2
# Find the middle row to centre win
rowmid = int(rows / 2)
# Leave a black border
cols = cols - 2
# Find the middle column to cente win
colmid = int(cols / 2)
# Space out the menu items
if int(cols / 6) <= 16:
    delta = int(cols / 6)
else:
    # But not too far apart
    delta = 16


def banner(stdscr, clear, message):
    def line(y, x):
        stdscr.addstr(y, 1, '=' * x, curses.A_BOLD | curses.A_REVERSE)

    if clear:
        stdscr.clear()
    if message == 'header':
        line(1, cols)
        msg = f'{"CloudCIX Pod/PodNet Install Utility         Version Date: 26th April. 2024":^{cols}}'
        stdscr.addstr(2, 1, msg, curses.A_BOLD | curses.A_REVERSE)
        line(3, cols)
    elif message == 'agree':
        line(33, cols)
        stdscr.addstr(34, 1, f'{"Press Enter to Agree and Continue...":^{cols}}', curses.A_BOLD | curses.A_REVERSE)
        line(35, cols)

    stdscr.refresh()


def display_errors(second_win, error_list):
    second_win.refresh()
    errors = len(error_list)
    if errors > 0:
        second_win.addstr(1, 2, f' {str(len(error_list))} errors found... ', curses.color_pair(3))
        for x in range(0, errors):
            second_win.addstr(3 + x, 2, error_list[x])
    second_win.addstr(13, 1, 'Press any key to exit the installer.', curses.color_pair(2))
    second_win.refresh()
    stdscr.getch()
    exit(1)


def setup_windows():
    # Make sure the screen is big enough
    if (rows < 35) or (cols < 90):
        raise ScreenTooSmallError('Screen is too small')

    # Clear keyboard inputs that may have been entered by user during delay screen.
    curses.flushinp()

    # Define the size and position for main window
    win = curses.newwin(23, 84, 5, colmid - 42)

    # Define the size and position for the first sub-window
    first_win_rows = 9
    first_win_cols = 84
    first_win_y = 0  # Start at the top of the large window
    first_win_x = 0  # Start at the left edge of the large window

    # Define the size and position for the second sub-window
    second_win_rows = 23 - first_win_rows  # Remaining rows
    second_win_cols = 84
    second_win_y = first_win_rows  # Start at the row just below the first sub-window
    second_win_x = 0  # Start at the left edge of the large window

    # Create the first sub-window
    first_win = win.subwin(first_win_rows, first_win_cols, 5 + first_win_y, colmid - 42 + first_win_x)

    # Create the second sub-window
    second_win = win.subwin(second_win_rows, second_win_cols, 5 + second_win_y, colmid - 42 + second_win_x)

    return win, first_win, second_win


def copyright(stdscr):
    banner(stdscr, True, 'header')
    win = curses.newwin(23, 84, 5, colmid - 42)
    with open(f'{directory}/copyright.txt') as file:
        copyright_text = file.read()
    try:
        win.addstr(1, 1, copyright_text)
        banner(stdscr, False, 'agree')
    except curses.error:
        pass
    win.refresh()
    user_input = stdscr.getkey()
    while user_input != '\n':
        user_input = win.getkey()


def main(stdscr):
    # First copyright
    copyright(stdscr)

    # The Procedure
    banner(stdscr, True, 'header')
    win, first_win, second_win = setup_windows()
    # Add some text to the first sub-window
    first_win.addstr(0, 0, "Level 1: Tests:", curses.A_BOLD)

    # Add some text to the second sub-window
    second_win.addstr(0, 0, "Level 1: Errors:", curses.A_BOLD)

    # 1. i,ii,iii,iv  Determine the  Installer state and Hardware state compatibility
    first_win.addstr(1, 1, 'Test (1.1): Determining the Installer state:')
    first_win.refresh()
    time.sleep(1)
    all_hostnames = ['podnet-a', 'podnet-b', 'appliance']
    hostname = socket.gethostname()

    if hostname not in all_hostnames:
        first_win.addstr(1, 1, 'Test (1.1): Determining the Installer state        :FAILED', curses.color_pair(3))
        first_win.refresh()
        message = f"Invalid hostname: {hostname}. NOT a valid installer state."
        second_win.addstr(1, 1, message, curses.color_pair(3))
        second_win.addstr(13, 1, 'Press any key to exit the installer.', curses.color_pair(2))
        second_win.refresh()
        stdscr.getch()
        exit(1)

    installer_type = 'podnet' if 'podnet' in hostname else 'appliance'
    first_win.addstr(1, 1, f'Test (1.1): Determining the Installer state        :"{hostname}" Installation ', curses.color_pair(4))

    # 1.2 Validate config.json
    first_win.addstr(2, 1, 'Test (1.2): Validating config.json file.')
    first_win.refresh()
    time.sleep(1)
    valid_config, error_list = validate_config(installer_type)
    if not valid_config:
        first_win.addstr(2, 1, 'Test (1.2): Validating config.json file             :FAILED', curses.color_pair(3))
        first_win.refresh()
        display_errors(second_win, error_list)
    first_win.addstr(2, 1, 'Test (1.2): Validating config.json file            :PASSED', curses.color_pair(4))

    # 1.3 Validate host hardware
    first_win.addstr(3, 1, 'Test (1.3): Validating host hardware compatibility.')
    first_win.refresh()
    time.sleep(1)
    valid_hardware, error_list = validate_hardware(installer_type)
    if not valid_hardware:
        first_win.addstr(3, 1, 'Test (1.3): Validating host hardware compatibility :FAILED', curses.color_pair(3))
        first_win.refresh()
        display_errors(second_win, error_list)
    first_win.addstr(3, 1, 'Test (1.3): Validating host hardware compatibility :PASSED', curses.color_pair(4))

    # 1.4 Validate host software
    first_win.addstr(4, 1, 'Test (1.4): Validating host software compatibility.')
    first_win.refresh()
    time.sleep(1)
    valid_software, error_list = validate_software(installer_type)
    if not valid_software:
        first_win.addstr(4, 1, 'Test (1.4): Validating host software compatibility :FAILED', curses.color_pair(3))
        first_win.refresh()
        display_errors(second_win, error_list)
    first_win.addstr(4, 1, 'Test (1.4): Validating host software compatibility :PASSED', curses.color_pair(4))

    first_win.addstr(8, 1, 'Press any key to exit the installer.', curses.color_pair(2))
    first_win.refresh()
    stdscr.getch()
    exit(1)


try:
    curses.wrapper(main)
except ScreenTooSmallError as e:
    print(str(e))
