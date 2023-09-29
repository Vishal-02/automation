import tkinter as tk
from tkinter import ttk
from tkinter import filedialog as f

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
        label.grid(row=0, column=2, padx=70, pady=70, columnspan=2, sticky="n")

        # button for split
        button1 = ttk.Button(self, text="Split", width=20,
                             command=lambda:controller.show_frame(Split))
        button1.grid(row=1, column=1, padx=30, pady=30, sticky="n")

        # button for merge
        button2 = ttk.Button(self, text="Merge", width=20,
                             command=lambda:controller.show_frame(Merge))
        button2.grid(row=1, column=2, padx=30, pady=30, sticky="n")

        # button for encrypt
        button3 = ttk.Button(self, text="Encrypt", width=20,
                             command=lambda:controller.show_frame(Merge))
        button3.grid(row=1, column=3, padx=30, pady=30, sticky="n")

        # button for decrypt
        button4 = ttk.Button(self, text="Decrypt", width=20,
                             command=lambda:controller.show_frame(Merge))
        button4.grid(row=1, column=4, padx=30, pady=30, sticky="n")

class Split(tk.Frame):
    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)
        self.file_name = ""

        label = ttk.Label(self, text="   Split PDF", font=("Times New Roman", 25))
        label.grid(row=0, column=2, padx=70, pady=70, columnspan=2, sticky="n")

        button1 = ttk.Button(self, text="Choose the file you wish to upload", width=40,
                             command=self.upload_file)
        button1.grid(row=1, column=1, padx=30, pady=30, sticky="n")

        self.fillerLabel = ttk.Label(self, width=100, text="", font=("Times New Roman", 10))
        self.fillerLabel.grid(row=1, column=2, padx=30, pady=30)

        button2 = ttk.Button(self, text="Page 2", width=20,
                             command=lambda:controller.show_frame(Merge))
        button2.grid(row=1, column=3, padx=30, pady=30)

        fillerLabel2 = ttk.Label(self, text="     ", width=20, font=("Times New Roman", 15))
        fillerLabel2.grid(row=1, column=4, padx=30, pady=30)

    def upload_file(self):
        file_types = [('PDF Files', 'pdf')]
        file_name = f.askopenfilename(filetypes=file_types, initialdir="C:/Users/USER/Downloads")
        file_name = file_name.split('\\')[-1]
        self.fillerLabel.configure(text=file_name)
        self.fillerLabel.update()

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
