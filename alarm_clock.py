# Alarm Clock - a simple clock where it plays a sound after X number
# of minutes/seconds or at a particular time.

import tkinter as tk
from time import strftime
from tkinter import ttk
from winsound import PlaySound
from winsound import SND_ASYNC
from winsound import SND_FILENAME
from winsound import SND_PURGE

clock_on = True


# Functions
def show_current_time():
    """Function to show current time"""
    time_string = strftime('%I:%M:%S %p')
    time_label.config(text=time_string)
    time_label.after(1000, show_current_time)


def play_sound():
    """
    Function to play sound when time runs out
    Music from https://www.bensound.com/
    """
    if pick_tune.get() == 'Tune 1 - Ukelele':
        return PlaySound('bensound_ukelele.wav', SND_FILENAME | SND_ASYNC)
    return PlaySound('bensound_happyrock.wav', SND_FILENAME | SND_ASYNC)


def start_countdown():
    input_time = int(pick_hour.get()) * 3600 + int(pick_minute.get()) * 60 + int(pick_second.get())
    while input_time >= 0:
        # divmod(firstvalue = input_time//60, secondvalue = input_time%60)
        mins, secs = divmod(input_time, 60)
        hours = 0
        if mins > 60:
            hours, mins = divmod(mins, 60)

        yield hours, mins, secs
        input_time -= 1


def reset_countdown_label():
    """
    Updates the countdown label every second
    """
    global clock_on
    clock_on = True
    PlaySound(None, SND_PURGE)
    set_alarm_btn["state"] = "disabled"
    description_lbl.config(text="Timer set")
    current_countdown = start_countdown()

    def set_label_recursively():
        if clock_on:
            try:
                time_hours, time_mins, time_secs = next(current_countdown)
                timer_string = f"{time_hours:02d}:{time_mins:02d}:{time_secs:02d}"
                countdown_lbl.config(text=timer_string)
                countdown_lbl.after(1000, set_label_recursively)
            except StopIteration:
                set_alarm_btn["state"] = "normal"
                play_sound()
        else:
            set_alarm_btn["state"] = "normal"
            return

    set_label_recursively()


def stop_button():
    """Stops the timer/alarm buzzer"""
    global clock_on
    clock_on = False
    PlaySound(None, SND_PURGE)


def reset():
    """Resets the program"""
    stop_button()
    countdown_lbl.config(text="00:00:00")
    description_lbl.config(text="Set an Alarm or Timer and get things done!")
    pick_hour.current(0)
    pick_minute.current(0)
    pick_second.current(0)
    pick_am_pm.current(0)
    start_timer_btn["state"] = "normal"
    pick_tune.current(0)


def set_alarm():
    """Function to set alarm clock"""
    stop_button()
    start_timer_btn["state"] = "disabled"
    description_lbl.config(text="Alarm set for")

    if pick_hour.get() == '00':
        adjusted_hour = '12'
    else:
        adjusted_hour = pick_hour.get()

    entered_time = f"{adjusted_hour}:{pick_minute.get()}:{pick_second.get()} {pick_am_pm.get()}"
    countdown_lbl.config(text=entered_time)

    def check_alarm():
        if entered_time != strftime('%I:%M:%S %p'):
            countdown_lbl.after(1000, check_alarm)
        else:
            start_timer_btn["state"] = "normal"
            play_sound()

    check_alarm()


# Creating tkinter window
master = tk.Tk()
master.title("Alarm Clock/Timer")

# Creating current time label
time_label = ttk.Label(master, font=("calibri", 35, "bold"), width=14, anchor="center",
                       background="black", foreground="white")
time_label.grid(row=0, column=0, pady=10, columnspan=4)
show_current_time()

# Creating hour/minute/second/AM-PM labels
hour_lbl = ttk.Label(master, text="Hours", font=("calibri", 14, "bold"))
hour_lbl.grid(row=1, column=0, pady=5)

minute_lbl = ttk.Label(master, text="Minutes", font=("calibri", 14, "bold"))
minute_lbl.grid(row=1, column=1, pady=5)

second_lbl = ttk.Label(master, text="Seconds", font=("calibri", 14, "bold"))
second_lbl.grid(row=1, column=2, pady=5)

am_pm_label = ttk.Label(master, text="AM/PM", font=("calibri", 14, "bold"))
am_pm_label.grid(row=1, column=3, pady=5)

# Combobox creation
hour = tk.StringVar()
minute = tk.StringVar()
second = tk.StringVar()
am_pm = tk.StringVar()

# Adding hour drop down list
pick_hour = ttk.Combobox(master, width=5, textvariable=hour, font=("calibri", 14))
pick_hour['values'] = ('00', '01', '02', '03',
                       '04', '05', '06', '07',
                       '08', '09', '10', '11', '12')
pick_hour.grid(column=0, row=2, padx=5, pady=5)
pick_hour.current(0)

# Adding minute drop down list
pick_minute = ttk.Combobox(master, width=5, textvariable=minute, font=("calibri", 14))
pick_minute['values'] = ('00', '05', '10', '15',
                         '20', '25', '30', '35',
                         '40', '45', '50', '55')
pick_minute.grid(column=1, row=2, padx=5, pady=5)
pick_minute.current(0)

# Adding second drop down list
pick_second = ttk.Combobox(master, width=5, textvariable=second, font=("calibri", 14))
pick_second['values'] = ('00', '05', '10', '15',
                         '20', '25', '30', '35',
                         '40', '45', '50', '55')
pick_second.grid(column=2, row=2, padx=5, pady=5)
pick_second.current(0)

# Adding AM/PM drop down
pick_am_pm = ttk.Combobox(master, width=5, textvariable=am_pm, font=("calibri", 14))
pick_am_pm['values'] = ('AM', 'PM')
pick_am_pm.grid(column=3, row=2, padx=5, pady=5)
pick_am_pm.current(0)

# Creating start timer button
start_timer_btn = tk.Button(master, text="Start Timer", bg="#d1d1d1", width=18, command=lambda: reset_countdown_label())
start_timer_btn.grid(row=3, column=0, columnspan=2, pady=10)

# Creating stop timer button
stop_buzzer_btn = tk.Button(master, text="Stop Buzzer", bg="#f7f2f2", width=18, command=lambda: stop_button())
stop_buzzer_btn.grid(row=4, column=0, columnspan=2, pady=10)

# Creating set alarm button
set_alarm_btn = tk.Button(master, text="Set Alarm", bg="#d1d1d1", width=18, command=lambda: set_alarm())
set_alarm_btn.grid(row=3, column=2, columnspan=2, pady=10)

# Tunes combobox
tunes = tk.StringVar()
pick_tune = ttk.Combobox(master, state="readonly", width=16, textvariable=tunes, font=("calibri", 12))
pick_tune['values'] = ('Tune 1 - Ukelele', 'Tune 2 - Happy Rock')
pick_tune.grid(column=2, row=4, columnspan=2, pady=10)
pick_tune.current(0)

# Creating description label
description_lbl = ttk.Label(master, text="Set an Alarm or Timer and get things done!",
                            font=("calibri", 12, "bold"))
description_lbl.grid(row=5, column=0, pady=5, columnspan=4)

# Creating timer label
countdown_lbl = ttk.Label(master, font=("calibri", 35, "bold"), width=14,
                          anchor="center", background="black", foreground="white")
countdown_lbl.grid(row=6, column=0, pady=5, padx=10, columnspan=4)

# Quit button to quit program
quit_button = tk.Button(master, text="QUIT", bg="red", fg="white", width=18, command=master.destroy)
quit_button.grid(row=7, column=0, pady=10, columnspan=2)

# Creating reset button
reset_btn = tk.Button(master, text="RESET", bg="#d1d1d1", width=18, command=lambda: reset())
reset_btn.grid(row=7, column=2, pady=10, columnspan=2)

if __name__ == "__main__":
    # Setting default time at 0
    countdown_lbl.config(text=f"00:00:00")
    tk.mainloop()
