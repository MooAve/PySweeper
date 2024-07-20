import time
import random
import os



menu = True



while menu:
    f = open("scores.txt", "r")
    line = f.readline()
    f.close()

    if line.isnumeric():
        # Sort high scores from highest to lowest 
        f = open("scores.txt", "w")
        f.write("30 120 180")
        f.close()