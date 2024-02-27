import customtkinter as ck
import tkinter.ttk as ttk
import tkinter as tk

ck.set_appearance_mode("System")
ck.set_default_color_theme("dark-blue")

window = ck.CTk()
window.title("PDF Controller")
# window.geometry("800x600")

def handle_keypress(event):
    print(event.char, end="")

window.bind("<Key>", handle_keypress)

window.mainloop()