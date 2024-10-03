import tkinter as tk
from tkinter import ttk
from tkinter import StringVar

# GLOBAL VARIABLES / CONSTANTS

GLOBAL_FONT = "Segoe UI"
GLOBAL_FONT_SIZE = 20
GLOBAL_FONT_SIZE_LARGE = 28
GRID_DIM = 3  # 3x3 Grid System (Dimensions)
PALETTE = ["#72BF78", "#A0D683", "#D3EE98", "#FEFF9F", '#6C757D']

def main():
    
    # Local Functions
    def grid_window(window):  # This function configures grid weight
        for i in range(GRID_DIM):
            window.grid_rowconfigure(i, weight=1)  # ith Row
            window.grid_columnconfigure(i, weight=1)  # ith Column

    
    def create_task():
        
        def save_task():
            print(task_input.get())
            create_task_window.destroy()
        create_task_window = tk.Toplevel(window)
        create_task_window.title("Create a task")
        create_task_window.minsize(800,600)  # Minumum width and height
        grid_window(create_task_window)
        task_name = StringVar()
        task_input = tk.Entry(create_task_window,
                    bg=COLOR["primary_entry"]["bg"],
                    fg=COLOR["primary_entry"]["fg"],
                    bd=0,
                    font=(GLOBAL_FONT, GLOBAL_FONT_SIZE),
                    textvariable=task_name
                    )
        save_task_btn = tk.Button(create_task_window,
                    command=save_task,
                    bg=COLOR["primary_btn"]["bg"],
                    fg=COLOR["primary_btn"]["fg"],
                    font=(GLOBAL_FONT, GLOBAL_FONT_SIZE),
                    relief='flat',
                    text='Save',
                    pady=2,
                    padx=4)
        save_task_btn.grid(row=2, column=1, sticky="N")
        task_input.grid(row=1, column=1, sticky="")
        task_input.focus_force()
    # Configure Window

    window = tk.Tk()

    window.title("Todo Be")
    window.state('zoomed')  # Start maximized
    window.minsize(800,600)  # Minumum width and height

    # Configure style

    style = ttk.Style()
    style.configure('main.TLabel', font=('Segoe UI', GLOBAL_FONT_SIZE), foreground=PALETTE[4])
    style.configure('main_large.TLabel', font=('Segoe UI', GLOBAL_FONT_SIZE_LARGE), foreground=PALETTE[4])
    
    # Basically a seperate styling for button because buttons don't work well in ttk

    COLOR = {
        "primary_btn": {
            "bg": PALETTE[1],
            "fg": "white"
        },

        "primary_entry": {
            "bg": PALETTE[2],
            "fg": PALETTE[4]
        }
    }

    # Configure grid

    grid_window(window)

    welcome_label = ttk.Label(window, text="Welcome to Todo Be!", style="main_large.TLabel")
    welcome_label.grid(row=0, column=1, sticky="")
    create_task_btn = tk.Button(window,
                    command=create_task,
                    bg=COLOR["primary_btn"]["bg"],
                    fg=COLOR["primary_btn"]["fg"],
                    font=(GLOBAL_FONT, GLOBAL_FONT_SIZE),
                    relief='flat',
                    text='Create',
                    pady=2,
                    padx=4)
    create_task_btn.grid(row=2, column=1, sticky="N")

    add_task_label = ttk.Label(window, text="First of all, please create your first task!", style="main.TLabel")
    add_task_label.grid(row=1, column=1, sticky="")

    window.mainloop()


if __name__ == "__main__":
    main()