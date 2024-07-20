#Avery Moore
#CS361-400
#Minesweeper Project - GameBoard

import tkinter as tk
from tkinter import Toplevel
from tkinter import messagebox
from tkinter import ttk
import time
import random

tiles = []
num_mines = 0
num_flags = 0
remaining_tiles = 0
first_click = True
has_won = False


class timer(ttk.Frame):
    """
    Represents a timer object
    Code adapted from https://stackhowto.com/how-to-make-a-timer-in-python-tkinter/
    """
    def __init__(self, frame):
        """
        Initialize the timer
        Requires a tkinter frame as a parameter
        """
        ttk.Frame.__init__(self, frame)
        self.start_time = time.time()
        self.cur_time = self.start_time
        self.clock = ttk.Label(frame, text="BLBLBLB", font=("Calibri", 16))
        self.clock.grid(column=2, row=0)

        self.update_time()

    def update_time(self):
        """
        Updates the time displayed on the 'timer' object
        """
        self.cur_time = time.time() - self.start_time

        try:
            self.clock.configure(text=time.strftime("%M:%S", time.localtime(self.cur_time)))
        except:
            print("Clock destroyed during time update, stopping clock...")
            return

        self.after(1000, self.update_time)


class board(ttk.Frame):
    """
    Creates the main game board
    """
    def __init__(self, frame, canvas_size, board_size, mine_total):
        """
        Initiates the main game board
        Requires a tkinter frame as a parameter
        Also requires the size of the board and number of mines for the board
        """
        ttk.Frame.__init__(self, frame)
        self.game_board = tk.Canvas(frame, width=canvas_size[0], height=canvas_size[1])
        self.game_board.place(x=0, y=40)
        self.game_ended = False
        self._board_size = board_size

        random.seed()

        self.set_globals(mine_total)
        create_tiles(self, board_size)


    def set_globals(self, mine_total):
        """
        Initiates the global variables
        """

        global tiles
        tiles = []

        global num_mines
        num_mines = mine_total

        global remaining_tiles
        tile_num = self._board_size[0] * self._board_size[1]
        remaining_tiles = tile_num - num_mines

        if remaining_tiles <= 0:
            remaining_tiles = 1
            num_mines = tile_num - 1

        global first_click
        first_click = True

        global num_flags
        num_flags = mine_total

        global has_won
        has_won = False


class box(tk.Canvas):
    """
    Creates a single tile on the board
    """

    def __init__(self, board, pos):
        tk.Canvas.__init__(self, board.game_board)
        self._posx = pos[0]
        self._posy = pos[1]
        startx = self._posx * 15
        starty = self._posy * 15
        endx = startx + 15
        endy = starty + 15
        self.canvas = board.game_board
        self.tile = self.canvas.create_rectangle(startx, starty, endx, endy, fill="gray", tag="tile")
        self.board = board

        self.cleared = False
        self.flagged = False
        self.contents = 0

        self.canvas.tag_bind(self.tile, "<Button-1>", self.clear_tile)
        self.canvas.tag_bind(self.tile, "<Button-3>", self.place_flag)

    def check_mines(self):
        """
        Sets the number of adjacent mines for each surrounding tile
        Sets content to numbers 1-8 to indicate if mines are adjacent
        """

        for i in range(-1, 2):
            cur_row = self._posy + i
            if 0 <= cur_row < len(tiles):
                for j in range(-1, 2):
                    cur_col = self._posx + j
                    if 0 <= cur_col < len(tiles[cur_row]):
                        cur_tile = tiles[cur_row][cur_col]
                        if cur_tile.contents != "mine":
                            cur_tile.contents += 1

    def generate_mines(self):
        """
        Generates mines randomly throughout the board
        """

        mine_count = 0
        while mine_count < num_mines:
            rand_row = random.randrange(0, len(tiles))
            rand_col = random.randrange(0, len(tiles[0]))
            rand_tile = tiles[rand_row][rand_col]

            if rand_tile.contents != "mine" and not rand_tile.cleared:
                rand_tile.contents = "mine"
                rand_tile.check_mines()
                mine_count += 1

    def adjacent_clear(self):
        """
        Checks any tiles above, below, and to the left and right of the current one
        Calls clear_tile on any non-mine tile
        """

        # Clear any safe adjacent tiles if they exist
        if self._posy - 1 >= 0:
            cur_tile = tiles[self._posy - 1][self._posx]
            if cur_tile.contents != "mine":
                cur_tile.clear_tile("<Button-1>")

        if self._posy + 1 < len(tiles):
            cur_tile = tiles[self._posy + 1][self._posx]
            if cur_tile.contents != "mine":
                cur_tile.clear_tile("<Button-1>")

        if self._posx - 1 >= 0:
            cur_tile = tiles[self._posy][self._posx - 1]
            if cur_tile.contents != "mine":
                cur_tile.clear_tile("<Button-1>")

        if self._posx + 1 < len(tiles[self._posy]):
            cur_tile = tiles[self._posy][self._posx + 1]
            if cur_tile.contents != "mine":
                cur_tile.clear_tile("<Button-1>")


    def game_over(self):
        """
        Displays a message and shows the full board once the game has ended
        """

        global has_won
        if has_won:
            messagebox.showinfo(title="Congratulations!", message="You Win!")
        else:
            messagebox.showerror(title="Game Over", message="You Lost...")

        self.board.game_ended = True

    def clear_tile(self, click):
        """
        Clears tile and displays its contents when it is clicked
        Also clears any safe adjacent tiles
        """

        global first_click

        if not self.cleared and not self.flagged:

            if self.contents == "mine":
                self.canvas.itemconfig(self.tile, fill="red")
                self.game_over()

            else:
                # Clear tile and display contents
                self.canvas.itemconfig(self.tile, fill="white")

                self.cleared = True

                global remaining_tiles
                remaining_tiles -= 1

                # Generate mines on first click, prevents first click loss
                if first_click:
                    self.generate_mines()
                    first_click = False

                # Check if there are no more tiles to clear
                if remaining_tiles <= 0:
                    global has_won
                    has_won = True
                    self.game_over()

                # Display number of adjacent mines if there are any
                if self.contents != 0:
                    self.canvas.create_text(self._posx * 15 + 8, self._posy * 15 + 8, text=str(self.contents))

                self.adjacent_clear()


    def place_flag(self, click):
        """
        Toggles a flag on the tile when right-clicked
        """

        global num_flags

        if not self.cleared:
            if self.flagged:
                self.canvas.itemconfig(self.tile, fill="gray")
                self.flagged = False
                num_flags += 1
            elif num_flags > 0:
                self.canvas.itemconfig(self.tile, fill="orange")
                self.flagged = True
                num_flags -= 1


def create_tiles(canvas, size):
    """
    Given a tkinter canvas and an array containing width and height,
    generates the number of tiles with the given dimensions and stores them in an array
    """

    # Initialize tiles and 2D array to store each tile's data
    for i in range(size[1]):
        row = []
        for j in range(size[0]):
            new_tile = box(canvas, (j, i))
            row.append(new_tile)
        tiles.append(row)

    return





