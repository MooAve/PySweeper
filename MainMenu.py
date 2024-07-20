#Avery Moore
#CS361-400
#Minesweeper Project - MainMenu

from tkinter import *
from tkinter import messagebox
from tkinter import ttk
import time
import GameBoard

adv_shown = "Hide"
lives = 0

def adv_toggle():
    """
    Shows/hides the advanced options on click
    """
    global adv_shown

    if adv_shown == "Hide":
        adv_btn.config(text = "Advanced Options >")
        adv_options.grid(column=0, row=7)
        adv_shown = "Show"
    else:
        adv_btn.config(text = "Advanced Options v")
        adv_options.grid_remove()
        adv_shown = "Hide"

    return


def reopen_menu(screen=None):
    """
    Reopens the main menu when previous menu has been closed
    Closes previous frame specified by screen
    """
    main.deiconify()
    if screen is not None:
        screen.destroy()

    return


def load_rules():
    """
    Loads the 'rules' menu
    Gets contents from rules.txt
    """

    # Hide the main menu
    main.withdraw()

    # Initial window setup
    rules = Toplevel(main)
    rules.grid()

    # Load Header
    ttk.Label(rules, text="Rules", font=("Calibri", 20)).grid(column=0, row=0)
    ttk.Separator(rules, orient="horizontal").grid(column=0, row=1, sticky="ew", columnspan=6)

    # Read rules from "rules.txt
    with open("rules.txt", "r") as f:
        rules_text = f.read()

    ttk.Label(rules, text=rules_text).grid(column=0, row=2)

    # Create 'back' button
    ttk.Button(rules, text="Back", command=lambda : reopen_menu(rules)).grid(column=0, row=3)

    rules.mainloop()

    return


def confirm_close(board):
    """
    Opens a confirmation box when closing game board
    """
    message = "Are you sure you wish to go back? Progress will be lost!"
    confirmation = messagebox.askokcancel(board, message=message)

    if confirmation:
        reopen_menu(board)

    return


def load_scores(timer, board):
    """
    Command to run when player has won or lost
    Stores the time to win in scores.txt if they won, closes the game board, and displays the leaderboard
    """
    cur_time = timer.cur_time

    if cur_time == 0:
        return

    str_time = time.strftime("%S", time.localtime(cur_time))

    with open("scores.txt", "r+") as f:
        f.write(str_time)

    board.destroy()

    scores = Toplevel(main)
    ttk.Label(scores, text="Best Times", font=("Calibri", 20)).grid(column=1, row=0)
    with open("scores.txt", "r") as f:
        best_times = f.read()

    ttk.Label(scores, text=best_times).grid(row=1)

    back_btn = ttk.Button(scores, text="Back to Menu", command=lambda: reopen_menu(scores))
    back_btn.grid(column=0, row=0)

    scores.mainloop()

    return


def load_board():
    """Loads the main game board"""
    # Hide the main menu
    main.withdraw()

    # Initial window setup
    board = Toplevel(main)

    # Load Header
    ttk.Label(board, text="Main Board", font=("Calibri", 20)).grid(column=1, row=0)
    ttk.Separator(board, orient="horizontal").grid(column=0, row=1, sticky="ew", columnspan=6)
    ttk.Label(board, text="This is where the main board should be").grid(column=0, row=2)

    # Create 'back' button
    ttk.Button(board, text="Back", command=lambda: confirm_close(board)).grid(column=0, row=0)

    # Create Board
    global width, height
    timer = GameBoard.timer(board)
    board_size = (width.get(), height.get())
    game_board = GameBoard.board(board, (500, 500), board_size, num_mines.get())

    while not game_board.game_ended and board.winfo_exists():
        board.update_idletasks()
        board.update()

    # Load scores if game ended naturally (i.e. not via "back" button)
    if board.winfo_exists():
        load_scores(timer, board)

    return


def check_size(text_input):
    """
    Used to check if input in board size entry box is an int
    If so, checks if digit is in range
    """

    if text_input.isdigit():
        if 0 < int(text_input) <= 30:
            return True

    message = "Please input a number between 1 and 30"
    messagebox.showerror(title="Input Error", message=message)
    return False


def check_mines(text_input):
    """
    Used to check if text in number of mines entry box is an int
    If so, checks if digit is in range
    """

    if text_input.isdigit():
        if 0 < int(text_input) < 900:
            return True

    message = "Please input a number between 1 and 899"
    messagebox.showerror(title="Input Error", message=message)
    return False


def set_difficulty():
    """
    Changes the number of mines and board size based on the selected difficulty
    Settings are not changed if manually edited by "advanced options"
    """
    global difficulty, num_mines, width, height, size_set, mine_set
    dif_str = difficulty.get()

    size_is_set = size_set.get()
    mine_is_set = mine_set.get()

    if dif_str == "easy":
        if size_is_set == 0:
            width.set(value=5)
            height.set(value=5)
        if mine_is_set == 0:
            num_mines.set(value=10)
    elif dif_str == "med":
        if size_is_set == 0:
            width.set(value=10)
            height.set(value=10)
        if mine_is_set == 0:
            num_mines.set(value=30)
    elif dif_str == "hard":
        if size_is_set == 0:
            width.set(value=20)
            height.set(value=20)
        if mine_is_set == 0:
            num_mines.set(value=125)

    return


def toggle_size_option(width_entry, height_entry):
    """
    Toggles the advanced board size option
    """

    global size_set
    if size_set.get() == 1:
        width_entry.configure(state="normal")
        height_entry.configure(state="normal")
    else:
        width_entry.configure(state="disabled")
        height_entry.configure(state="disabled")
        set_difficulty()

    return


def toggle_mine_option(mine_entry):
    """
    Toggles the advanced mine number option
    """

    global mine_set
    if mine_set.get() == 1:
        mine_entry.configure(state="normal")
    else:
        mine_entry.configure(state="disabled")
        set_difficulty()

    return


# Initial window setup
main = Tk()
mm_frame = Frame()
mm_frame.grid()
theme = StringVar()

# Set default game settings, equivalent to "Medium" difficulty
difficulty = StringVar(value="med")
width = IntVar(value=10)
height = IntVar(value=10)
num_mines = IntVar(value=30)
size_set = IntVar(value=0)
mine_set = IntVar(value=0)

style = ttk.Style()
style.theme_use("clam")

# Style Configurations
style.configure("TRadiobutton", font=("Calibri", 16))
style.configure("Adv.TButton", foreground="cornflowerblue", activeforeground="blue")
style.configure("Adv.TButton", font=("Calibri", 16), bd=0, activebackground="white")
style.configure("Play.TButton", background="red", foreground="white", font=("Calibri", 14))

# Load Header
ttk.Label(mm_frame, text="Minesweeper", font=("Calibri", 20)).grid(column=1, row=0)
ttk.Separator(mm_frame, orient="horizontal").grid(column= 0, row=1, sticky="ew", columnspan=6)

# Load Exit and "How to Play" buttons
ttk.Button(mm_frame, text="Exit", command=lambda: main.destroy()).grid(column=0, row=0)
ttk.Button(mm_frame, text="How to Play", command=load_rules).grid(column=1, row=2)

# Load theme selection
ttk.Label(mm_frame, text="Theme", font=("Calibri", 18)).grid(column=0,row=3)
l_theme = ttk.Radiobutton(mm_frame, text="Light", style="TRadiobutton")
l_theme.configure(variable=theme, value="light_theme")
l_theme.grid(column=0, row=5)

d_theme = ttk.Radiobutton(mm_frame, text="Dark", style="TRadiobutton")
d_theme.configure(variable=theme, value="dark_theme")
d_theme.grid(column=1, row=5)

# Load advanced options toggle
adv_btn=ttk.Button(mm_frame, text="Advanced Options v", style="Adv.TButton", command=adv_toggle)
adv_btn.grid(column=0, row=6)

adv_options = ttk.LabelFrame(mm_frame)

# Load custom board size options
size_entry_check = adv_options.register(check_size)
mine_entry_check = adv_options.register(check_mines)

width_entry = ttk.Entry(adv_options, textvariable=width, state="disabled")
width_entry.configure(validate="focusout", validatecommand=(size_entry_check, "%P"))
width_entry.grid(row=9, column=0)

ttk.Label(adv_options, text="X").grid(row=9, column=1)
height_entry = ttk.Entry(adv_options, textvariable=height, state="disabled")
height_entry.configure(validate="focusout", validatecommand=(size_entry_check, "%P"))
height_entry.grid(row=9, column=2)

size_check = ttk.Checkbutton(adv_options, text="Custom Board Size", style="TRadiobutton")
size_check.configure(variable=size_set, command=lambda: toggle_size_option(width_entry, height_entry))
size_check.grid(row=8, column=0)

# Load custom mine count option and life options
ttk.Entry(adv_options).grid(row=11, column=2)
ttk.Checkbutton(adv_options, text="Lives", style="TRadiobutton").grid(row=10, column=2)

mine_entry = ttk.Entry(adv_options, textvariable=num_mines, state="disabled")
mine_entry.configure(validate="focusout", validatecommand=(mine_entry_check, "%P"))
mine_entry.grid(row=11, column=0)

mine_check = ttk.Checkbutton(adv_options, text="Number of Mines", style="TRadiobutton")
mine_check.configure(variable=mine_set, command=lambda: toggle_mine_option(mine_entry))
mine_check.grid(row=10, column=0)

# Load difficulty select and play button
easy_button = ttk.Radiobutton(mm_frame, text="Easy",  style="TRadiobutton")
easy_button.configure(variable=difficulty, value="easy", command=set_difficulty)
easy_button.grid(column=0, row=12)

med_button = ttk.Radiobutton(mm_frame, text="Medium",  style="TRadiobutton")
med_button.configure(variable=difficulty, value="med", command=set_difficulty)
med_button.grid(column=1, row=12)

hard_button = ttk.Radiobutton(mm_frame, text="Hard", style="TRadiobutton")
hard_button.configure(variable=difficulty, value="hard", command=set_difficulty)
hard_button.grid(column=2, row=12)
ttk.Button(mm_frame, text="Play", style="Play.TButton", command=load_board).grid(column=1, row=13)

main.mainloop()
