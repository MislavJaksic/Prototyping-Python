"""
    protopy.py
    ------------------

    Runs the project.

    :copyrgiht: 2019 MislavJaksic
    :license: MIT License
"""
import sys
from tkinter import Tk, ttk, StringVar, N, W, E, S


class FeetToMeters:
    def __init__(self, root):
        self.root = root
        self.configure_root()
        self.mainframe = self.make_frame()

        self.feet = StringVar()
        self.meters = StringVar()
        self.feet_entry = self.make_entry()

        ttk.Label(self.mainframe, textvariable=self.meters).grid(column=2, row=2, sticky=(W, E))
        ttk.Button(self.mainframe, text="Calculate", command=self.calculate).grid(column=3, row=3, sticky=W)

        ttk.Label(self.mainframe, text="feet").grid(column=3, row=1, sticky=W)
        ttk.Label(self.mainframe, text="is equivalent to").grid(column=1, row=2, sticky=E)
        ttk.Label(self.mainframe, text="meters").grid(column=3, row=2, sticky=W)

        for child in self.mainframe.winfo_children():
            child.grid_configure(padx=5, pady=5)

    def make_frame(self):
        mainframe = ttk.Frame(self.root, padding="3 3 12 12")
        mainframe.grid(column=0, row=0, sticky=(N, W, E, S))
        return mainframe

    def calculate(self):
        try:
            value = float(self.feet.get())
            self.meters.set(int(0.3048 * value * 10000.0 + 0.5) / 10000.0)
        except ValueError:
            pass

    def configure_root(self):
        self.root.title("Feet to Meters")
        self.root.columnconfigure(0, weight=1)
        self.root.rowconfigure(0, weight=1)
        self.root.attributes("-topmost", True)
        # self.root.wm_attributes("-transparentcolor", "white")
        # self.root.attributes('-alpha', 0.5)
        self.root.bind("<Return>", self.calculate)

    def make_entry(self):
        feet_entry = ttk.Entry(self.mainframe, width=7, textvariable=self.feet)
        feet_entry.grid(column=2, row=1, sticky=(W, E))
        return feet_entry


def main(args):
    """main() will be run if you run this script directly"""
    root = Tk()
    FeetToMeters(root)
    root.mainloop()


def run():
    """Entry point for the runnable script."""
    sys.exit(main(sys.argv[1:]))


if __name__ == "__main__":
    """main calls run()."""
    run()
