import tkinter as tk
from tkinter import ttk
from tkinter import StringVar, IntVar

# GLOBAL VARIABLES / CONSTANTS

GLOBAL_FONT = "Segoe UI"
GLOBAL_FONT_SIZE = 20
GLOBAL_FONT_SIZE_LARGE = 28
GRID_DIM = 3  # 3x3 Grid System (Dimensions)
PALETTE = ["#72BF78", "#A0D683", "#D3EE98", "#FEFF9F", '#6C757D']
COLOR = {
    "primary_btn": {
        "bg": PALETTE[1],
        "fg": "white"
    },

    "primary_entry": {
        "bg": PALETTE[2],
        "fg": PALETTE[4]
    },
    "low_priority": "#28a745",
    "mid_priority": "#ffc107",
    "high_priority": "#dc3545",
    "error": "#dc3545"
}

def main():
    
    # Local Functions
    def grid_window(window):  # This function configures grid weight
        for i in range(GRID_DIM):
            window.grid_rowconfigure(i, weight=1)  # ith Row
            window.grid_columnconfigure(i, weight=1)  # ith Column

    
    def create_task():
        
        def task_input_error(error):  # this function is called when there is an error with user input
            # Error Codes
            # no task name is 0
            # no priority is 1

            # Configuring error_task_window

            error_task_window = tk.Toplevel(create_task_window)
            error_task_window.title("Error")
            error_task_window.minsize(600,300)
            grid_window(error_task_window)
            # Make the window modal (user must close it before interacting with main window)
            error_task_window.grab_set()
            error_task_window.transient(create_task_window)  # Keep the error window on top of the main window

            error_task_label = ttk.Label(error_task_window, style="error.TLabel")
            error_task_label.grid(row=1, column=1, sticky="")

            error_task_btn = tk.Button(error_task_window,
                    command=error_task_window.destroy,
                    bg=COLOR["error"],
                    fg=COLOR["primary_btn"]["fg"],
                    font=(GLOBAL_FONT, GLOBAL_FONT_SIZE),
                    relief='flat',
                    text='OK',
                    pady=1,
                    padx=1)
            error_task_btn.grid(row=2, column=1, sticky="")

            if error == 0:
                error_task_label.configure(text="Please enter the task name.")
            elif error == 1:
                error_task_label.configure(text="Please select a priority.")


        def save_task():

            if task_name.get().isspace() or task_name.get() == "":
                return task_input_error(0)
            if priority_var.get() == -1:
                return task_input_error(1)
            print(task_name.get(), priority_var.get())
            create_task_window.destroy()


        create_task_window = tk.Toplevel(window)
        create_task_window.title("Create a task")
        create_task_window.minsize(800,600)  # Minumum width and height
        grid_window(create_task_window)
        task_name = StringVar()

        name_label = ttk.Label(create_task_window, style="main.TLabel", text="Name")  # Just indicating that this is a name input
        name_label.grid(row=0, column=0, sticky="e")

        task_input = tk.Entry(create_task_window,
                    bg=COLOR["primary_entry"]["bg"],
                    fg=COLOR["primary_entry"]["fg"],
                    bd=0,
                    font=(GLOBAL_FONT, GLOBAL_FONT_SIZE),
                    textvariable=task_name
                    )
        task_input.grid(row=0, column=1, sticky="")

        priority_var = IntVar(value=-1)  # initializing IntVar with -1 so it doesn't automatically select priority

        task_priority_low = ttk.Radiobutton(create_task_window, variable=priority_var, style="low_priority.TRadiobutton", text="Low-priority", value=0)
        task_priority_low.grid(row=1, column=0, sticky="e")

        task_priority_mid = ttk.Radiobutton(create_task_window, variable=priority_var, style="mid_priority.TRadiobutton", text="Middle-priority", value=1)
        task_priority_mid.grid(row=1, column=1, sticky="")
        
        task_priority_high = ttk.Radiobutton(create_task_window, variable=priority_var, style="high_priority.TRadiobutton", text="High-priority", value=2)
        task_priority_high.grid(row=1, column=2, sticky="w")

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

        task_input.focus_force()
    # Configure Window

    window = tk.Tk()

    window.title("Todo Be")
    window.state('zoomed')  # Start maximized
    window.minsize(800,600)  # Minumum width and height

    # Configure style

    style = ttk.Style()
    style.configure('main.TLabel', font=(GLOBAL_FONT, GLOBAL_FONT_SIZE), foreground=PALETTE[4])
    style.configure('error.TLabel', font=(GLOBAL_FONT, GLOBAL_FONT_SIZE_LARGE), foreground=COLOR["error"])
    style.configure('main_large.TLabel', font=(GLOBAL_FONT, GLOBAL_FONT_SIZE_LARGE), foreground=PALETTE[4])
    style.configure('low_priority.TRadiobutton', font=(GLOBAL_FONT, GLOBAL_FONT_SIZE, "bold"), foreground=COLOR["low_priority"])
    style.configure('mid_priority.TRadiobutton', font=(GLOBAL_FONT, GLOBAL_FONT_SIZE, "bold"), foreground=COLOR["mid_priority"])
    style.configure('high_priority.TRadiobutton', font=(GLOBAL_FONT, GLOBAL_FONT_SIZE, "bold"), foreground=COLOR["high_priority"])

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