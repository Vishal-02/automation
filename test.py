import tkinter as tk
from tkinter import ttk

window = tk.Tk()
window.title("Address Entry Form")

titles = [
    "First Name", "Last Name", "Address Line 1", "Address Line 2", "City", "State", "Province", "Postal Code", "Country"
]

# frame = tk.Frame(borderwidth=5, relief=tk.SUNKEN)
# frame.pack()

for _, title in enumerate(titles):

    label = tk.Label(master=window, text=f"{title}:")
    entry = tk.Entry(master=window, width=70)

    label.grid(row=_, column=0, sticky="e")
    entry.grid(row=_, column=1)

    


window.mainloop()
        