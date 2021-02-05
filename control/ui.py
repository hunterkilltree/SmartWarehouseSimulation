from tkinter import *
import tkinter as tk



def handle_move_click():
    print("This is handle move click")


def handle_generate_click():
    print("This is handle generate click")


def handle_start_click():
    print("This is handle start click")


def handle_stop_click():
    print("This is handle stop click")


def handle_reset_click():
    print("This is handle reset click")


def handle_exit_click():  # quit programming so this method not use
    print("This is handle exit click")


def handle_drop_down_menu(choice):
    print("This is " + choice)


def handle_check_button(txt):  # 1: check; 2: uncheck
    print("This is " + txt)


class Application(tk.Tk):

    def __init__(self):
        super().__init__()

        self.title("ControlUI")
        self.iconbitmap("image/Robot2.ico")
        self.geometry("650x100")

        self.clicked = StringVar()
        self.var = StringVar()

    def button_move(self):
        button = Button(self, text="Move", command=handle_move_click)
        button.grid(row=0, column=0)

    def button_generate(self):
        button = Button(self, text="Generate", command=handle_generate_click)
        button.grid(row=0, column=1)

    def button_start(self):
        button = Button(self, text="Start", command=handle_start_click)
        button.grid(row=0, column=2)

    def button_stop(self):
        button = Button(self, text="Stop", command=handle_stop_click)
        button.grid(row=0, column=3)

    def button_reset(self):
        button = Button(self, text="Reset", command=handle_reset_click)
        button.grid(row=0, column=4)

    def button_exit(self):
        button = Button(self, text="Exit", command=self.quit)
        button.grid(row=0, column=5)

    def drop_down_menu(self):
        options = [
            "List options",
            "Start coordinate",
            "Goal coordinate",
            "Obstacle Coordinate",
            "Station Coordinate"
        ]

        self.clicked.set(options[0])

        drop = OptionMenu(self, self.clicked, *options)
        self.clicked.trace('w', self.data_drop_menu)
        drop.grid(row=0, column=6)

    def check_button(self):
        c = Checkbutton(self, text="Auto", variable=self.var, onvalue="On", offvalue="Off")
        c.deselect()  # not select by default
        c.grid(row=0, column=7)
        self.var.trace('w', self.data_check_button)

    def text_box(self, robot, goal):

        frame1 = LabelFrame(self, text="Robot coordinate", padx=10, pady=10)
        frame1.grid(row=0, column=8)
        robotPos = Label(frame1, text=robot)
        robotPos.grid(row=0, column=0)

        frame2 = LabelFrame(self, text="Goal coordinate", padx=10, pady=10)
        frame2.grid(row=0, column=9)
        goalPos = Label(frame2, text=goal)
        goalPos.grid(row=0, column=0)

    def notification(self):
        pass

    def data_drop_menu(self, *a):
        handle_drop_down_menu(self.clicked.get())

    def data_check_button(self, *a):
        handle_check_button(self.var.get())

        self.text_box(0, 0)
