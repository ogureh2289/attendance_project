import tkinter as tk
from tkinter import *

from controller import create_student

root = tk.Tk()
root.title("Интерфейс")

tk.Label(root, text="ФИО").grid(row=0, column=0, padx=5, pady=5)
entry_fio = tk.Entry( width=30)
entry_fio.grid(row=0, column=1, padx=5, pady=5)

tk.Label(root, text="Класс").grid(row=1, column=0, padx=5, pady=5)
entry_class = tk.Entry(width=30)
entry_class.grid(row=1, column=1, padx=5, pady=5)

tk.Label(root, text="Email").grid(row=2, column=0, padx=5, pady=5)
entry_email = tk.Entry(width=30)
entry_email.grid(row=2, column=1, padx=5, pady=5)

submit_button = tk.Button(text="Отправить",
                          command=create_student(entry_fio.get(), entry_class.get(), entry_email.get()))
submit_button.grid(row=3, columnspan=2, pady=10)

root.mainloop()
