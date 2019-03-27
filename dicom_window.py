from tkinter import *
from dicom import save_dicom

class Dicom_Window(Toplevel):
    def __init__(self, parent):
        Toplevel.__init__(self, parent)
        self.parent = parent
        self.title("DICOM")
        self.grab_set()

        self.file = StringVar()
        self.name = StringVar()
        self.age = StringVar()
        self.weight = StringVar()
        self.sex = StringVar()
        self.comment = StringVar()

        self.file.set("new")
        self.name.set("N/N")
        self.sex.set("N/N")

        self.file_entry = Entry(self, textvariable=self.file)
        self.name_entry = Entry(self, textvariable=self.name)
        self.age_entry = Entry(self, textvariable=self.age)
        self.weight_entry = Entry(self, textvariable=self.weight)
        self.sex_entry = Entry(self, textvariable=self.sex)
        self.comment_text = Text(self, height=10, width=15)

        self.save_button = Button(self, text="Save", command=self.save)

        self.set_widgets()


    def set_widgets(self):
        self.file_label = Label(self, text="Filename").grid(column=0, row=0)
        self.file_entry.grid(column=1, row=0)

        self.name_label = Label(self, text="Name").grid(column=0, row=1)
        self.name_entry.grid(column=1, row=1)
        self.name_entry.grid(column=1, row=1)

        self.sex_label = Label(self, text="Sex").grid(column=0, row=2)
        self.sex_entry.grid(column=1, row=2)

        self.age_label = Label(self, text="Age").grid(column=0, row=3)
        self.age_entry.grid(column=1, row=3)

        self.weight_label = Label(self, text="Weight").grid(column=0, row=4)
        self.weight_entry.grid(column=1,row=4)

        self.comment_label = Label(self, text="Comment").grid(column=0, row=5)
        self.comment_text.grid(column=1, row=5)

        self.save_button.grid(column=1, row=6)


    def get_variables(self):
        self.name = str(self.name_entry.get())
        self.age = str(self.age_entry.get())
        self.weight = str(self.weight_entry.get())
        self.sex = str(self.sex_entry.get())
        self.comment = str(self.comment_text.get('1.0', END))

        return self.name, self.age, self.weight, self.sex, self.comment


    def save(self):
        save_dicom(filename=str(self.file_entry.get()), patient=self.get_variables(), image=self.parent.inverse)
        self.destroy()
        print("saved as dicom")















