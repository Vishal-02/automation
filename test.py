import tkinter as tk
from tkinter import ttk
import pdf_functions as p

class base_app(tk.Tk):
    def __init__(self, *args, **kwargs) -> None:
        tk.Tk.__init__(self, *args, **kwargs)

        # create a container
        container = tk.Frame(self)
        container.pack(side="top", fill="both", expand=True)

        container.grid_columnconfigure(0, weight=1)
        container.grid_rowconfigure(0, weight=1)

        self.frames = {}

        for _ in (StartPage, FirstPage, SecondPage):
            frame = _(container, self)
            self.frames[_] = frame

            frame.grid(row=0, column=0, sticky="nsew")

        self.show_frame(StartPage)

    def show_frame(self, cont):
        frame = self.frames[cont]
        frame.tkraise()


class StartPage(tk.Frame):
    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)

        label = ttk.Label(self, text="Main Menu")
        label.grid(row=0, column=4, padx=10, pady=10)

        button1 = ttk.Button(self, text="Page 1",
                             command=lambda:controller.show_frame(FirstPage))
        button1.grid(row=1, column=1, padx=10, pady=10)

        button2 = ttk.Button(self, text="Page 2",
                             command=lambda:controller.show_frame(SecondPage))
        button2.grid(row=2, column=1, padx=10, pady=10)
        

class FirstPage(tk.Frame):
    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)
        label = ttk.Label(self, text="first page")
        label.grid(row=0, column=4, padx=10, pady=10)

        button1 = ttk.Button(self, text="Start Page",
                             command=lambda:controller.show_frame(StartPage))
        button1.grid(row=1, column=1, padx=10, pady=10)

        button2 = ttk.Button(self, text="Page 2",
                             command=lambda:controller.show_frame(SecondPage))
        button2.grid(row=2, column=1, padx=10, pady=10)

class SecondPage(tk.Frame):
    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)
        label = ttk.Label(self, text="second page")
        label.grid(row=0, column=4, padx=10, pady=10)

        button1 = ttk.Button(self, text="Start Page",
                             command=lambda:controller.show_frame(StartPage))
        button1.grid(row=1, column=1, padx=10, pady=10)

        button2 = ttk.Button(self, text="Page 1",
                             command=lambda:controller.show_frame(FirstPage))
        button2.grid(row=2, column=1, padx=10, pady=10)


app = base_app()
app.mainloop()