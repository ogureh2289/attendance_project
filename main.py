import tkinter as tk

def on_button_click(text):


    root = tk.Tk()
    root.title("Интерфейс")

    tk.Label(root, text="ФИО").grid(row=0, column=0, padx=5, pady=5)
    entry_fio = tk.Entry(root, width=30)
    entry_fio.grid(row=0, column=1, padx=5, pady=5)

    tk.Label(root, text="Класс").grid(row=1, column=0, padx=5, pady=5)
    entry_class = tk.Entry(root, width=30)
    entry_class.grid(row=1, column=1, padx=5, pady=5)

    tk.Label(root, text="Email").grid(row=2, column=0, padx=5, pady=5)
    entry_email = tk.Entry(root, width=30)
    entry_email.grid(row=2, column=1, padx=5, pady=5)

    generate_qr = tk.Button(root, text="Генерация QR-кода", command=lambda: on_button_click("Генерация QR"))

    generate_qr.grid(row=4, column=1, padx=5, pady=10)

    root.mainloop()