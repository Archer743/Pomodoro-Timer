import time
import threading
import pygame
import tkinter as tk
from tkinter import ttk, PhotoImage


class PomodoroTimer:
    def __init__(self):
        # Creates a window with a size, name and icon <-> UI - User Interface
        self.root = tk.Tk()
        self.root.geometry("600x300")
        self.root.title("Pomodoro Timer")
        self.root.tk.call('wm', 'iconphoto', self.root._w, PhotoImage(file="Pictures/tomato.png"))
        
        # Style
        self.s = ttk.Style()
        self.s.configure("TNotebook.Tab", font=("Ubuntu", 16))  # font - Ubuntu, font size - 16 -> this is for the tab look
        self.s.configure("TButton", font=("Ubuntu", 16))  # font - Ubuntu, font size - 16 -> this is for the button look

        # Tabs
        self.tabs = ttk.Notebook(self.root)
        self.tabs.pack(fill="both", pady=10, expand=True)  # pady - padding on y-axis
        
        self.tab1 = ttk.Frame(self.tabs, width=600, height=100)  # Pomodoro    Tab
        self.tab2 = ttk.Frame(self.tabs, width=600, height=100)  # Short Break Tab
        self.tab3 = ttk.Frame(self.tabs, width=600, height=100)  # Long  Break Tab

        # Labels
        self.pomodoro_timer_label = ttk.Label(self.tab1, text="25:00", font=("Ubuntu", 48))
        self.pomodoro_timer_label.pack(pady=20)

        self.short_break_timer_label = ttk.Label(self.tab2, text="05:00", font=("Ubuntu", 48))
        self.short_break_timer_label.pack(pady=20)

        self.long_break_timer_label = ttk.Label(self.tab3, text="15:00", font=("Ubuntu", 48))
        self.long_break_timer_label.pack(pady=20)

        # Adds every tab to the tabs' section
        self.tabs.add(self.tab1, text="Pomodoro")
        self.tabs.add(self.tab2, text="Short Break")
        self.tabs.add(self.tab3, text="Long Break")

        # Grid Layout
        self.grid_layout = ttk.Frame(self.root)
        self.grid_layout.pack(pady=10)

        # Buttons
        self.start_button = ttk.Button(self.grid_layout, text="Start", command=self.start_timer_thread)
        self.start_button.grid(row=0, column=0)

        self.skip_button = ttk.Button(self.grid_layout, text="Skip", command=self.skip_clock)
        self.skip_button.grid(row=0, column=1)

        self.reset_button = ttk.Button(self.grid_layout, text="Reset", command=self.reset_clock)
        self.reset_button.grid(row=0, column=2)
        
        # Functionality Variables
        self.pomodoros = 0
        self.last_tab_index = 0
        self.running = False
        self.skipped = False
        self.stopped = False

        # Music
        pygame.mixer.init()  # pygame provides a music mixer that can play music

        # Settings
        # ...

        # Pomodoro Counter
        self.pomodoro_counter_label = ttk.Label(self.grid_layout, text=f"Pomodoros: {self.pomodoros}", font=("Ubuntu", 16))
        self.pomodoro_counter_label.grid(row=1, column=0, columnspan=3, pady=10)

        # Runs the application
        self.root.mainloop()

    def start_timer_thread(self):
        if not self.running:
            t = threading.Thread(target=self.start_timer)  # We use this so the timer can be updated while we move the window
            t.start()
            self.running = True


    def start_timer(self):
        self.stopped = False
        self.skipped = False
        timer_id = self.last_tab_index

        if timer_id == 0:
            self.timer(5, 0)
            
            if not self.stopped or self.skipped:
                self.pomodoros += 1
                self.pomodoro_counter_label.config(text=f"Pomodoros: {self.pomodoros}")  # Updates the pomodoro_counter_label's view
                
                if not self.stopped:
                    self.audio_play()

                if self.pomodoros % 4 == 0:
                    self.tabs.select(2)  # Selects the long break tab
                    self.last_tab_index = 2
                else:
                    self.tabs.select(1)  # Selects the short break tab
                    self.last_tab_index = 1

                self.start_timer()

        elif timer_id == 1:
            self.timer(5, 1)

            if not self.stopped or self.skipped:
                if not self.stopped:
                    self.audio_play()

                self.tabs.select(0)  # Selects the pomodoro tab
                self.last_tab_index = 0
                self.start_timer()

        elif timer_id == 2:
            self.timer(5, 2)

            if not self.stopped or self.skipped:
                if not self.stopped:
                    self.audio_play()

                self.tabs.select(0)  # Selects the pomodoro tab
                self.last_tab_index = 0
                self.start_timer()

        else:
            print("Tab index out of range!")

    def reset_clock(self):
        self.pomodoros = 0
        self.last_tab_index = 0
        self.running = False
        self.skipped = False
        self.stopped = True

        self.pomodoro_timer_label.config(text="25:00")
        self.short_break_timer_label.config(text="05:00")
        self.long_break_timer_label.config(text="15:00")
        self.pomodoro_counter_label.config(text=f"Pomodoros: {self.pomodoros}")

    def skip_clock(self):
        cur_timer_id = self.last_tab_index

        if cur_timer_id == 0:
            self.pomodoro_timer_label.config(text="25:00")
            if self.pomodoros % 4 == 0:
                self.tabs.select(2)
                self.last_tab_index = 2
            else:
                self.tabs.select(1)
                self.last_tab_index = 1

        elif cur_timer_id == 1:
            self.short_break_timer_label.config(text="05:00")
            self.tabs.select(0)
            self.last_tab_index = 0

        elif cur_timer_id == 2:
            self.long_break_timer_label.config(text="15:00")
            self.tabs.select(0)
            self.last_tab_index = 0

        self.stopped = True
        self.skipped = True

    
    def timer(self, full_seconds:int, tab:int):
        while full_seconds and not self.stopped:
            minutes, seconds = divmod(full_seconds, 60)  # Gets the minutes and the remaining seconds from full_seconds
            
            text=f"{minutes:02d}:{seconds:02d}"
            
            if tab == 0:   # Updates the timer view in the current tab
                self.pomodoro_timer_label.config(text=text)
            elif tab == 1:
                self.short_break_timer_label.config(text=text)
            else:
                self.long_break_timer_label.config(text=text)
            
            self.root.update()  # Updates the window
            time.sleep(1)
            full_seconds -= 1
        
        if not self.stopped:
            if tab == 0:   # Updates the timer view in the current tab
                self.pomodoro_timer_label.config(text="00:00")
            elif tab == 1:
                self.short_break_timer_label.config(text="00:00")
            else:
                self.long_break_timer_label.config(text="00:00")

    def get_timer_id(self):
        return self.tabs.index(self.tabs.select())  # Returns the index of the current tab / self.tabs.select() -> returns the last selected tab

    def audio_play(self):
        pygame.mixer.music.load("Audio/ring.mp3")
        pygame.mixer.music.play(loops=0)


if __name__ == '__main__':
    PomodoroTimer()