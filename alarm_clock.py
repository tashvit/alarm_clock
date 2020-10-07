# Alarm Clock - a simple clock where it plays a sound after X number
# of minutes/seconds or at a particular time.


import tkinter as tk
from tkinter import ttk
from time import strftime
from typing import Any, Tuple, Generator
from winsound import PlaySound
from winsound import SND_FILENAME
from winsound import SND_ASYNC


def show_current_time():
    """Function to show current time"""
    time_string = strftime('%I:%M:%S %p')
    time_label.config(text=time_string)
    time_label.after(1000, show_current_time)


def play_sound():
    """
    Function to play sound when time runs out
    Free music from https://www.bensound.com/
    """
    return PlaySound("bensound.wav", SND_FILENAME | SND_ASYNC)


def start_timer():
    """Function to start countdown"""
    input_time = int(pick_hour.get()) * 3600 + int(pick_minute.get()) * 60 + int(pick_second.get())

    while input_time >= 0:
        # divmod(firstvalue = input_time//60, secondvalue = input_time%60)
        mins, secs = divmod(input_time, 60)
        hours = 0
        if mins > 60:
            hours, mins = divmod(mins, 60)

        yield hours, mins, secs
        input_time -= 1


def start_button():
    """Function to control start timer button"""
    try:
        time_hours, time_mins, time_secs = next(set_time)
        timer_string = f"{time_hours:02d}:{time_mins:02d}:{time_secs:02d}"
        countdown_lbl.config(text=timer_string)
        countdown_lbl.after(1000, start_button)
    except StopIteration:
        play_sound()


# Creating tkinter window
master = tk.Tk()
master.title("Alarm Clock")

# Creating current time label
time_label = ttk.Label(master, font=("calibri", 30, "bold"),
                       background="black", foreground="white")
time_label.grid(row=0, column=0, pady=5, columnspan=3)
show_current_time()

# Creating hour/minute/second labels
hour_lbl = ttk.Label(master, text="Hours", font=("calibri", 15, "bold"))
hour_lbl.grid(row=1, column=0, pady=5)

minute_lbl = ttk.Label(master, text="Minutes", font=("calibri", 15, "bold"))
minute_lbl.grid(row=1, column=1, pady=5)

second_lbl = ttk.Label(master, text="Seconds", font=("calibri", 15, "bold"))
second_lbl.grid(row=1, column=2, pady=5)

# Combobox creation
hour = tk.StringVar()
minute = tk.StringVar()
second = tk.StringVar()

# Adding hour drop down list
pick_hour = ttk.Combobox(master, width=5, textvariable=hour, font=("calibri", 14))
pick_hour['values'] = (' 00', ' 01', ' 02', ' 03',
                       ' 04', ' 05', ' 06', ' 07',
                       ' 08', ' 09', ' 10', ' 11', ' 12')
pick_hour.grid(column=0, row=2, padx=5, pady=5)
pick_hour.current(0)

# Adding minute drop down list
pick_minute = ttk.Combobox(master, width=5, textvariable=minute, font=("calibri", 14))
pick_minute['values'] = (' 00', ' 05', ' 10', ' 15',
                         ' 20', ' 25', ' 30', ' 35',
                         ' 40', ' 45', ' 50', ' 55')
pick_minute.grid(column=1, row=2, padx=5, pady=5)
pick_minute.current(0)

# Adding second drop down list
pick_second = ttk.Combobox(master, width=5, textvariable=second, font=("calibri", 14))
pick_second['values'] = (' 00', ' 05', ' 10', ' 15',
                         ' 20', ' 25', ' 30', ' 35',
                         ' 40', ' 45', ' 50', ' 55')
pick_second.grid(column=2, row=2, padx=5, pady=5)
pick_second.current(0)

# Creating /setting up start timer button
set_time: Generator[Tuple[int, int, int], Any, None] = start_timer()
timer_button = ttk.Button(master, text="Start Timer",
                          command=lambda: start_button())
timer_button.grid(row=3, column=1, pady=10)

# Creating timer label
countdown_lbl = ttk.Label(master, font=("calibri", 35, "bold"))
countdown_lbl.grid(row=4, column=0, pady=5, columnspan=3)

# Quit button to quit program
quit_button = tk.Button(master, text="QUIT", bg="red", fg="white", command=master.destroy)
quit_button.grid(row=5, column=1, ipadx=10, pady=10)


if __name__ == "__main__":
    # Setting default time at 0
    countdown_lbl.config(text=f"00 : 00 : 00")
    tk.mainloop()
