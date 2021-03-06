from tkinter import *
from skimage import color, io
import matplotlib.pyplot as plt
import numpy as np

from dicom import load_dicom
from tomography import radon, inverse_radon
from dicom_window import Dicom_Window


class Window(Frame):

    def __init__(self, master=None):
        Frame.__init__(self, master)
        self.master = master
        master.title("Tomograph")

        self.numberOfThreads = 8
        self.mask = [-30, 61, -30]
        self.image = []
        self.alpha = 0
        self.n = 0
        self.d = 0
        self.inverse = []

        self.image_var = StringVar()
        self.alpha_var = StringVar()
        self.n_var = StringVar()
        self.d_var = StringVar()
        self.is_filter = IntVar()
        self.is_iterative = IntVar()
        self.is_rescaled = IntVar()
        self.threads_var = IntVar()

        # default values
        self.image_var.set("Sin.png")
        self.alpha_var.set("1")
        self.n_var.set("100")
        self.d_var.set("180")
        self.threads_var.set(8)

        self.image_entry = Entry(self, textvariable=self.image_var)
        self.alpha_entry = Entry(self, textvariable=self.alpha_var)
        self.n_entry = Entry(self, textvariable=self.n_var)
        self.d_entry = Entry(self, textvariable=self.d_var)
        self.threads_entry = Entry(self, textvariable=self.threads_var)

        self.filter_check = Checkbutton(self, text="Filter", variable=self.is_filter)
        self.iterative_check = Checkbutton(self, text="Iterative", variable=self.is_iterative)
        self.stretch_rescale_check = Checkbutton(self, text="Rescale intensity", variable=self.is_rescaled)

        self.run_button = Button(self, text="Run", command=self.run_transform)
        self.dicom_button = Button(self, text="Save as DICOM", command=self.create_dicom_window)

        self.create_widgets()
        self.pack()


    def create_widgets(self):
        Label(self, text="Image").grid(row=0, column=0)
        self.image_entry.grid(row=0, column=1)

        Label(self, text="Threads").grid(row=1, column=0)
        self.threads_entry.grid(row=1, column=1)

        Label(self, text=" ").grid(row=2)

        # variables
        Label(self, text="Alpha").grid(row=3, column=0)
        self.alpha_entry.grid(row=3, column=1)
        Label(self, text="Detectors").grid(row=4, column=0)
        self.n_entry.grid(row=4, column=1)
        Label(self, text="Arc").grid(row=5, column=0)
        self.d_entry.grid(row=5, column=1)

        self.filter_check.grid(row=6, column=1)
        self.iterative_check.grid(row=7, column=1)
        self.stretch_rescale_check.grid(row=8, column=1)

        self.run_button.grid(row=9, column=1)
        self.dicom_button.grid(row=10, column=1)



    def run_transform(self, __=0):
        if self.get_variables() == -1:
            return
        self.grab_set()
        print("sinogram")
        sinogram, measures, fig = radon(self.image, self.n, self.alpha, self.d, self.numberOfThreads, self.mask, self.is_iterative.get(), self.is_rescaled.get())

        sino = np.copy(sinogram)
        self.inverse = inverse_radon(self.image, sino, self.n, self.alpha, self.d, self.numberOfThreads, fig, self.is_iterative.get(), self.is_rescaled.get())
        print("***")


    def get_variables(self):
        try:
            image_name = str(self.image_var.get())
            if image_name[-4:] == '.dcm':
                (self.image, patient) = load_dicom(image_name)
                dicom_window = Dicom_Window(self)
                dicom_window.load(image_name, patient)
            else:
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

    def create_dicom_window(self):
        dicom_window = Dicom_Window(self)


def start():
    print("starting gui")
    root = Tk()
    root.geometry("640x640")
    app = Window(root)
    app.mainloop()


