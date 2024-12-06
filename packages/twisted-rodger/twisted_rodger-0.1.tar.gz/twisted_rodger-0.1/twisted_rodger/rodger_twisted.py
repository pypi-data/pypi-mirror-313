import tkinter as tk
from tkinter import PhotoImage

def main():
    root = tk.Tk()
    root.title("rodher")
    try:
        img = PhotoImage(file="image.png")
    except Exception as e:
        print(f"eror. cant load rodher image")
        return
    label = tk.Label(root, image=img)
    label.pack()
    root.mainloop()