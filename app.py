import os
import json
import tkinter as tk
from tkinter import ttk, font
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
JSON_FILE_PATH = "tasks/0.json"

def main():
    
    # just check if the json file is empty or exists
    is_first_time = True

    if os.path.exists(JSON_FILE_PATH):

        is_first_time = False
        with open(JSON_FILE_PATH, "r") as json_file:
            try:
                data = json.load(json_file)
                if data == []:
                    is_first_time = True
            except:  # if the json file is empty
                is_first_time = True

    # Local Functions
    def grid_window(window, grid_dim=GRID_DIM, reset=False):  # This function configures grid weight
        if reset:
            cell_weight = 0  # resetting grid configuration
            refresh_tasks(window)  # kills all widgets

        else:
            cell_weight = 1
        for i in range(grid_dim):
            window.grid_rowconfigure(i, weight=cell_weight)  # ith Row
            window.grid_columnconfigure(i, weight=cell_weight)  # ith Column

    
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
            
            # checking if the directory for storing tasks exists

            if not os.path.exists("tasks"):
                os.makedirs("tasks")
            
            if not os.path.isfile(JSON_FILE_PATH):
                data = []
                # initializing data for storing json
            else:
                with open(JSON_FILE_PATH, "r") as json_file:
                    try:
                        data = json.load(json_file)
                    except:  # if the user trolls and deletes the json data
                        data = []
            
            # the new task to write
            new_task = {
                "name": task_name.get(),
                "priority": priority_var.get(),
                "done": 0
            }

            # appending new_task in the data list
            data.append(new_task)

            # write the new task in the json file
            with open(JSON_FILE_PATH, "w") as json_file:
                json.dump(data, json_file, indent=4)
            
            create_task_window.destroy()

            # clear the elements if first time

            if is_first_time:
                grid_window(window, reset=True)
                display_tasks()
            else:
                refresh_tasks(window)
                display_tasks()


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
    

    # this function helps truncate strings longer than 18 characters
    def truncate_string(text, max_length=18):
        if len(text) > max_length:
            return text[:max_length-3] + '...'  # Reserve space for '...'
        return text
    

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
    
    def first_time():  # this function is called when json file is empty or doesn't exist
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
    

    def refresh_tasks(window):
        for widget in window.winfo_children():
            widget.destroy()


    def display_tasks():

        # strike through font for done tasks

        STRIKE_THROUGH_FONT = font.Font(family=GLOBAL_FONT, size=GLOBAL_FONT_SIZE_LARGE, overstrike=True)
        style.configure('main_strike_large.TLabel', font=STRIKE_THROUGH_FONT, foreground=PALETTE[4])
        load_strike=ttk.Label(window, style="main_strike_large.TLabel")  # somehow without this line the whole strike through thing doesn't work
        # if there is no done tasks

        # Update the json file with checkbox state
        def update_task(id):
            with open(JSON_FILE_PATH, "w") as json_file:
                data[id]["done"] = done_var_dict[id].get()
                json.dump(data, json_file, indent=4)  # update the json file
            
            # Update the label font based on checkbox state (strikethrough if done, normal otherwise)
            if done_var_dict[id].get() == 1:
                task_label_dict[id].configure(style="main_strike_large.TLabel")  # Apply strikethrough
            else:
                task_label_dict[id].configure(style="main_large.TLabel")  # Remove strikethrough

        def delete_task(id):
            task_label_dict[id].destroy()
            check_label_dict[id].destroy()
            delete_task_dict[id].destroy()
            with open(JSON_FILE_PATH, "r+") as json_file:
                data = json.load(json_file)
                del data[id]
                json_file.seek(0)  # move the cursor to begining
                json.dump(data, json_file, indent=4)
                json_file.truncate()

                refresh_tasks(window)  # deletes all widgets
                if data == []:  # if there is no more tasks meaning all tasks deleted
                    window.grid_rowconfigure(0, weight=0)  # resets weight on row 0 before running first_time()
                    first_time()
                else:
                    display_tasks()

        # add a task button
        add_task_btn = tk.Button(window,
                        command=create_task,
                        bg=COLOR["primary_btn"]["bg"],
                        fg=COLOR["primary_btn"]["fg"],
                        font=(GLOBAL_FONT, GLOBAL_FONT_SIZE),
                        relief='flat',
                        text='Add a task',
                        pady=2,
                        padx=4)
        add_task_btn.place(relx=0.5, rely=0.1, anchor="center")

        with open(JSON_FILE_PATH, "r") as json_file:
            data = json.load(json_file)
            done_var_dict = {}  # a dict of done variables (storing the state of each checkbox)
            task_label_dict = {}  # a dict of labels of checkboxes
            delete_task_dict = {}  # a dict of delete buttons of checkboxes
            check_label_dict = {}  # a dict of checkboxes
            # iterate through checkboxes
            for i in range(len(data)):
                task = data[i]
                done_var_dict[i] = IntVar(value=data[i]["done"])
                
                if data[i]["done"] == 1:
                    task_label = ttk.Label(window, style="main_strike_large.TLabel", text=f"{i+1}. {truncate_string(task["name"])}  ")
                else:
                    task_label = ttk.Label(window, style="main_large.TLabel", text=f"{i+1}. {truncate_string(task["name"])}  ")

                task_label_dict[i] = task_label
                task_label.place(relx=0.01, rely=0.1 * (i+2), anchor="w")

                task_checkbox = ttk.Checkbutton(window, variable=done_var_dict[i], takefocus=False, command=lambda i=i: update_task(i))
                check_label_dict[i] = task_checkbox
                task_checkbox.place(relx=0.5, rely=0.1 * (i+2), anchor="center")

                delete_task_btn = tk.Button(window,
                                command=lambda i=i: delete_task(i),
                                fg=COLOR["error"],
                                font=(GLOBAL_FONT, GLOBAL_FONT_SIZE),
                                relief='flat',
                                text='✕'
                                ) 
                delete_task_dict[i] = delete_task_btn
                delete_task_btn.place(relx=0.95, rely=0.1 * (i+2), anchor="center")

    if is_first_time: first_time()
    else: display_tasks()
    
    window.mainloop()

if __name__ == "__main__":
    main()