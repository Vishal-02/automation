import tkinter as tk
from tkinter import ttk
from tkinter import filedialog as f
from PyPDF2 import PdfReader, PdfWriter
import pdf_functions as pdf_helper

"""
!!!!SUB-FRAMES!!!!
"""

class base_app(tk.Tk):
    def __init__(self, *args, **kwargs) -> None:
        tk.Tk.__init__(self, *args, **kwargs)

        # create a container
        container = tk.Frame(self)
        
        container.pack(side="top", fill="both", expand=True)

        container.grid_columnconfigure(3, weight=1)
        container.grid_rowconfigure(3, weight=1)

        self.frames = {}

        for _ in (StartPage, Split, Merge, Encrypt, Decrypt):
            frame = _(container, self)
            self.frames[_] = frame

            frame.grid(row=0, column=0, sticky="nesw", rowspan=5, columnspan=5)

        self.show_frame(StartPage)

    def show_frame(self, cont):
        frame = self.frames[cont]
        frame.tkraise()

class StartPage(tk.Frame):
    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)

        label = ttk.Label(self, text="   Welcome to PDF Splitter", font=("Times New Roman", 25))
        label.grid(row=0, column=2, padx=70, pady=70, columnspan=2, sticky="e")

        # button for split
        button1 = ttk.Button(self, text="Split", width=20,
                             command=lambda:controller.show_frame(Split))
        button1.grid(row=1, column=1, padx=50, pady=30, sticky="n")

        # button for merge
        button2 = ttk.Button(self, text="Merge", width=20,
                             command=lambda:controller.show_frame(Merge))
        button2.grid(row=1, column=2, padx=50, pady=30, sticky="n")

        # button for encrypt
        button3 = ttk.Button(self, text="Encrypt", width=20,
                             command=lambda:controller.show_frame(Merge))
        button3.grid(row=1, column=3, padx=50, pady=30, sticky="n")

        # button for decrypt
        button4 = ttk.Button(self, text="Decrypt", width=20,
                             command=lambda:controller.show_frame(Merge))
        button4.grid(row=1, column=4, padx=50, pady=30, sticky="n")

class Split(tk.Frame):
    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)
        self.file_name = "" # name of the file to be split
        self.first_page = tk.StringVar() # first page of the split
        self.last_page = tk.StringVar() # last page of the split

        # row 0
        label = ttk.Label(self, text="   Split PDF", font=("Times New Roman", 25))
        label.grid(row=0, column=1, padx=70, pady=70, columnspan=2, sticky="e")

        # ------------------------------------- row 1 ---------------------------------------------
        file_upload_button = ttk.Button(self, text="Choose the file you wish to upload", width=40,
                             command=self.upload_file)
        file_upload_button.grid(row=1, column=1, padx=30, pady=30, sticky="n")

        self.file_name_label = ttk.Label(self, width=35, text="", font=("Times New Roman", 13))
        self.file_name_label.grid(row=1, column=2, padx=30, pady=30)

        self.file_size = ttk.Label(self, text="", width=40, font=("Times New Roman", 13))
        self.file_size.grid(row=1, column=3, padx=30, pady=30)

        # ------------------------------------- row 2 ---------------------------------------------
        first_page_label = ttk.Label(self, text="Enter the first page: ",
                                font=("Times New Roman", 13))
        first_page_label.grid(row=2, column=1, padx=10, pady=10)

        first_page_value = tk.Entry(self, textvariable=self.first_page, font=("Times New Roman", 15))
        first_page_value.grid(row=2, column=2, padx=10, pady=10)

        last_page_label = ttk.Label(self, text="Enter the last page: ",
                                font=("Times New Roman", 13))
        last_page_label.grid(row=2, column=3, padx=10, pady=10)

        last_page_value = tk.Entry(self, textvariable=self.last_page, font=("Times New Roman", 15))
        last_page_value.grid(row=2, column=4, padx=10, pady=10)

        button2 = ttk.Button(self, text="Split", width=40,
                             command=self.split)
        button2.grid(row=3, column=2, padx=30, pady=30, sticky="e")

    def split(self):
        # if first page > no. of pages, empty pdf
        # if first page < no. of pages < last page, last page = no. of pages
        first_page = int(self.first_page.get())
        last_page = int(self.last_page.get())

        reader = PdfReader(pdf_helper.check_valid_file(self.file_name))
        num_of_pages = len(reader.pages)

        if first_page > num_of_pages or last_page <= 0:
            first_page = 0
            last_page = 0
        elif last_page > num_of_pages:
            last_page = num_of_pages

        # the part where we split the pdf, i'll try and modify the function in pdf_functions.py to work with this later as well
        writer = PdfWriter()
        for i in range(first_page - 1, last_page):
            writer.add_page(reader.pages[i])
        
        writer.write("C:/Users/visha/Documents/" + pdf_helper.add_extension(self.file_name))
        writer.close()
        

    def upload_file(self):
        file_types = [('PDF Files', 'pdf')]
        self.file_name = f.askopenfilename(filetypes=file_types, initialdir="shell:Downloads")
        self.file_size.configure(text=f"This document has {len(PdfReader(self.file_name).pages)} pages.")
        self.file_name = self.file_name.split('/')[-1]
        self.file_name_label.configure(text=self.file_name)
        self.file_name_label.update()

class Merge(tk.Frame):
    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)
        label = ttk.Label(self, text="second page")
        label.grid(row=0, column=1, padx=10, pady=10)

        button1 = ttk.Button(self, text="Start Page",
                             command=lambda:controller.show_frame(StartPage))
        button1.grid(row=1, column=1, padx=10, pady=10)

        button2 = ttk.Button(self, text="Page 1",
                             command=lambda:controller.show_frame(Split))
        button2.grid(row=2, column=1, padx=10, pady=10)

class Encrypt(tk.Frame):
    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)
        label = ttk.Label(self, text="Split PDF", font=("Times New Roman", 15))
        label.grid(row=0, column=1, padx=70, pady=70)

        button1 = ttk.Button(self, text="Start Page",
                             command=lambda:controller.show_frame(StartPage))
        button1.grid(row=1, column=1, padx=30, pady=30)

        button2 = ttk.Button(self, text="Page 2",
                             command=lambda:controller.show_frame(Merge))
        button2.grid(row=2, column=1, padx=10, pady=10)

class Decrypt(tk.Frame):
    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)
        label = ttk.Label(self, text="Split PDF", font=("Times New Roman", 15))
        label.grid(row=0, column=1, padx=70, pady=70)

        button1 = ttk.Button(self, text="Start Page",
                             command=lambda:controller.show_frame(StartPage))
        button1.grid(row=1, column=1, padx=30, pady=30)

        button2 = ttk.Button(self, text="Page 2",
                             command=lambda:controller.show_frame(Merge))
        button2.grid(row=2, column=1, padx=10, pady=10)

app = base_app()
app.mainloop()
