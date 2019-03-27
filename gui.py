from tkinter import *
from skimage import color, io
import matplotlib.pyplot as plt
import numpy as np
from tomography import radon, inverse_radon


class Window(Frame):

    def __init__(self, master=None):
        Frame.__init__(self, master)
        self.master = master
        master.title("Tomograph")

        self.numberOfThreads = 8
        self.mask = [-30, 61, -30]
        self.image = color.rgb2gray(io.imread('picbrain.jpg'))
        self.alpha = 0
        self.n = 0
        self.d = 0

        self.image_var = StringVar()
        self.alpha_var = StringVar()
        self.n_var = StringVar()
        self.d_var = StringVar()
        self.is_filter = IntVar()
        self.is_iterative = IntVar()
        self.threads_var = IntVar()

        self.image_entry = Entry(self, textvariable=self.image_var)
        self.alpha_entry = Entry(self, textvariable=self.alpha_var)
        self.n_entry = Entry(self, textvariable=self.n_var)
        self.d_entry = Entry(self, textvariable=self.d_var)
        self.threads_entry = Entry(self, textvariable=self.threads_var)

        self.run_button = Button(self)
        self.filter_check = Checkbutton(self, text="Filter", variable=self.is_filter)
        self.iterative_check = Checkbutton(self, text="Iterative", variable=self.is_iterative)

        self.create_widgets()
        self.pack()


    def create_widgets(self):
        Label(self, text="Image").grid(row=0, column=0)
        self.image_var.set("picbrain.jpg")
        self.image_entry.grid(row=0, column=1)

        Label(self, text="Threads").grid(row=1, column=0)
        self.threads_entry.grid(row=1, column=1)

        Label(self, text=" ").grid(row=2)

        # default values
        self.alpha_var.set("1")
        self.n_var.set("100")
        self.d_var.set("180")
        self.threads_var.set(8)

        # variables
        Label(self, text="Alpha").grid(row=3, column=0)
        self.alpha_entry.grid(row=3, column=1)
        Label(self, text="Detectors").grid(row=4, column=0)
        self.n_entry.grid(row=4, column=1)
        Label(self, text="Arc").grid(row=5, column=0)
        self.d_entry.grid(row=5, column=1)

        self.filter_check.grid(row=6, column=1)
        self.iterative_check.grid(row=7, column=1)

        self.run_button["text"] = "Run"
        self.run_button["command"] = self.run_transform
        self.run_button.grid(row=8, column=1)


    def run_transform(self, __=0):
        if self.set_variables() == -1:
            return
        self.grab_set()
        print("sinogram")
        sinogram, measures, fig = radon(self.image, self.n, self.alpha, self.d, self.numberOfThreads, self.mask, self.is_iterative.get())

        sino = np.copy(sinogram)
        inverse = inverse_radon(self.image, sino, self.n, self.alpha, self.d, self.numberOfThreads, fig, self.is_iterative.get())
        print("***")


    def set_variables(self):
        try:
            image_name = str(self.image_var.get())
            self.image = color.rgb2gray(io.imread(image_name))
        except:
            print("something wrong with the image")
            return -1
        try:
            self.numberOfThreads = int(self.threads_var.get())
        except:
            print("wrong format for number of threads")
            return -1
        try:
            self.alpha = float(self.alpha_var.get())
        except:
            print("wrong format for alpha")
            return -1
        try:
            self.n = int(self.n_var.get())
        except:
            print("wrong format for n")
            return -1
        try:
            self.d = int(self.d_var.get())
        except:
            print("wrong format for d")
            return -1

        if self.is_filter.get():
            self.mask = [-30, 61, -30]
        else:
            self.mask = [0, 1, 0]

        return 0

def start():
    print("starting gui")
    root = Tk()
    root.geometry("640x640")
    app = Window(root)
    app.mainloop()


start()