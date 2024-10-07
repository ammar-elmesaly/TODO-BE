import os
import json
import tkinter as tk
from tkinter import ttk, font
from tkinter import StringVar, IntVar

# GLOBAL VARIABLES / CONSTANTS

GLOBAL_FONT = "Segoe UI"
GLOBAL_FONT_SIZE = 20
GLOBAL_FONT_SIZE_LARGE = 28
GLOBAL_FONT_SIZE_MID = 24
GLOBAL_FONT_SIZE_SMALL = 18
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
            refresh_tasks(window)  # kills all widget8

        else:
            cell_weight = 1
        for i in range(grid_dim):
            window.grid_rowconfigure(i, weight=cell_weight)  # ith Row
            window.grid_columnconfigure(i, weight=cell_weight)  # ith Column

    
    def create_task():
        
        def task_input_error(error):  # this function is called when there is an error with user input
            # ====================== Error Codes ======================
            # no task name is 0
            # no priority is 1
            # character limit exceeded is 2
            # =========================================================

            # Configuring error_task_window

            error_task_window = tk.Toplevel(create_task_window)
            error_task_window.title("Error")
            error_task_window.minsize(600,300)
            error_task_window.resizable(False, False)  # Disable resizing window

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
            elif error == 2:
                error_task_label.configure(text="Name of the task must not exceed 60 characters.")


        def save_task():

            if task_name.get().isspace() or task_name.get() == "":
                return task_input_error(0)
            if priority_var.get() == -1:
                return task_input_error(1)
            if len(task_name.get()) > 60:
                return task_input_error(2)
            
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

            discription_text = task_discription.get("1.0", tk.END).replace("\n", "")
            if not discription_text.isspace() and not discription_text == "":
                new_task["discription"] = task_discription.get("1.0", tk.END)
            else:
                new_task["discription"] = ""

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
        create_task_window.resizable(False, False)  # Disable resizing window
        task_name = StringVar()

        name_label = ttk.Label(create_task_window, style="main.TLabel", text="Name")  # Just indicating that this is a name input
        name_label.place(relx=0.25, rely=0.1, anchor="center")

        task_input = tk.Entry(create_task_window,
                    bg=COLOR["primary_entry"]["bg"],
                    fg=COLOR["primary_entry"]["fg"],
                    bd=0,
                    font=(GLOBAL_FONT, GLOBAL_FONT_SIZE),
                    textvariable=task_name
                    )
        task_input.place(relx=0.5, rely=0.1, anchor="center")

        priority_var = IntVar(value=-1)  # initializing IntVar with -1 so it doesn't automatically select priority

        task_priority_low = ttk.Radiobutton(create_task_window, variable=priority_var, style="low_priority.TRadiobutton", text="Low-priority", value=0)
        task_priority_low.place(relx=0.2, rely=0.225, anchor="center")

        task_priority_mid = ttk.Radiobutton(create_task_window, variable=priority_var, style="mid_priority.TRadiobutton", text="Middle-priority", value=1)
        task_priority_mid.place(relx=0.5, rely=0.225, anchor="center")
        
        task_priority_high = ttk.Radiobutton(create_task_window, variable=priority_var, style="high_priority.TRadiobutton", text="High-priority", value=2)
        task_priority_high.place(relx=0.8, rely=0.225, anchor="center")

        discription_label = ttk.Label(create_task_window, style="main.TLabel", text="Discription (Optional)")  # Just indicating that this is a name input
        discription_label.place(relx=0.283, rely=0.35, anchor="center")

        task_discription = tk.Text(create_task_window,
                                height=5,
                                width=35,
                                fg=PALETTE[4],
                                font=(GLOBAL_FONT, GLOBAL_FONT_SIZE_MID)
                                )
        task_discription.place(relx=0.5, rely=0.6, anchor="center")

        save_task_btn = tk.Button(create_task_window,
                    command=save_task,
                    bg=COLOR["primary_btn"]["bg"],
                    fg=COLOR["primary_btn"]["fg"],
                    font=(GLOBAL_FONT, GLOBAL_FONT_SIZE),
                    relief='flat',
                    text='Save',
                    pady=2,
                    padx=4)
        save_task_btn.place(relx=0.5, rely=0.9, anchor="center")

        task_input.focus_force()
    

    # this function helps truncate strings longer than 18 characters
    def truncate_string(text, max_length=20):
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
    style.configure('error_small.TLabel', font=(GLOBAL_FONT, GLOBAL_FONT_SIZE_SMALL), foreground=COLOR["error"])
    style.configure('main_large.TLabel', font=(GLOBAL_FONT, GLOBAL_FONT_SIZE_LARGE), foreground=PALETTE[4])
    style.configure('main_mid.TLabel', font=(GLOBAL_FONT, GLOBAL_FONT_SIZE_MID), foreground=PALETTE[4])
    style.configure('discription.TLabel', font=(GLOBAL_FONT, GLOBAL_FONT_SIZE_MID), foreground=PALETTE[4], background=PALETTE[3])
    style.configure('low_priority.TRadiobutton', font=(GLOBAL_FONT, GLOBAL_FONT_SIZE, "bold"), foreground=COLOR["low_priority"])
    style.configure('mid_priority.TRadiobutton', font=(GLOBAL_FONT, GLOBAL_FONT_SIZE, "bold"), foreground=COLOR["mid_priority"])
    style.configure('high_priority.TRadiobutton', font=(GLOBAL_FONT, GLOBAL_FONT_SIZE, "bold"), foreground=COLOR["high_priority"])
    style.configure('low_priority.TLabel', font=(GLOBAL_FONT, GLOBAL_FONT_SIZE, "bold"), foreground=COLOR["low_priority"])
    style.configure('mid_priority.TLabel', font=(GLOBAL_FONT, GLOBAL_FONT_SIZE, "bold"), foreground=COLOR["mid_priority"])
    style.configure('high_priority.TLabel', font=(GLOBAL_FONT, GLOBAL_FONT_SIZE, "bold"), foreground=COLOR["high_priority"])
    
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
        # TODO TODO TODO
        # XXX Add edit functionality

        # strike through font for done tasks
        STRIKE_THROUGH_FONT = font.Font(family=GLOBAL_FONT, size=GLOBAL_FONT_SIZE_MID, overstrike=True)
        style.configure('main_strike_mid.TLabel', font=STRIKE_THROUGH_FONT, foreground=PALETTE[4])
        load_strike=ttk.Label(window, style="main_strike_mid.TLabel")  # somehow without this line the whole strike through thing doesn't work
        
        # underline discription button
        UNDERLINE_FONT = font.Font(family=GLOBAL_FONT, size=GLOBAL_FONT_SIZE_SMALL, underline=True) 

        # if there is no done tasks

        # Update the json file with checkbox state
        def update_task(id):
            with open(JSON_FILE_PATH, "w") as json_file:
                data[id]["done"] = done_var_dict[id].get()
                json.dump(data, json_file, indent=4)  # update the json file
            
            # Update the label font based on checkbox state (strikethrough if done, normal otherwise)
            if done_var_dict[id].get() == 1:
                task_label_dict[id].configure(style="main_strike_mid.TLabel")  # Apply strikethrough
            else:
                task_label_dict[id].configure(style="main_mid.TLabel")  # Remove strikethrough

        def delete_task(id, confirm_delete_window):
            confirm_delete_window.destroy()
            task_label_dict[id].destroy()
            check_label_dict[id].destroy()
            delete_task_dict[id].destroy()
            if show_discription_dict[id] != None:
                show_discription_dict[id].destroy()
            else:
                del show_discription_dict[id]
            priority_task_dict[id].destroy()

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
        

        def confirm_delete(id):
            confirm_delete_window = tk.Toplevel(window)
            confirm_delete_window.title("Confirm Delete")
            confirm_delete_window.minsize(task_label_dict[id].winfo_width() + 600, 300)  # fine tuning the minimum size relative to the task label width
            # Make the window modal (user must close it before interacting with main window)
            confirm_delete_window.grab_set()
            confirm_delete_window.transient(window)  # Keep the deletion confirm window on top of the main window

            confirm_delete_label = ttk.Label(confirm_delete_window,
                                            style="error.TLabel",
                                            text=f"Are you sure to delete this task ({truncate_string(data[id]["name"])})?")
            confirm_delete_label.place(relx=0.5, rely=0.2, anchor="center")

            confirm_delete_btn = tk.Button(confirm_delete_window,
                    command=lambda:delete_task(id, confirm_delete_window),
                    bg=COLOR["error"],
                    fg=COLOR["primary_btn"]["fg"],
                    font=(GLOBAL_FONT, GLOBAL_FONT_SIZE),
                    relief='flat',
                    text='OK',
                    pady=1,
                    padx=1)
            confirm_delete_btn.place(relx=0.43, rely=0.6, anchor="center")

            no_confirm_btn = tk.Button(confirm_delete_window,
                    command=confirm_delete_window.destroy,
                    bg=COLOR["primary_btn"]["bg"],
                    fg=COLOR["primary_btn"]["fg"],
                    font=(GLOBAL_FONT, GLOBAL_FONT_SIZE),
                    relief='flat',
                    text='NO',
                    pady=1,
                    padx=1)
            no_confirm_btn.place(relx=0.57, rely=0.6, anchor="center")
        
        # show discription of task

        def show_discription(id):
            discription_text = data[id]["discription"]
            discription_window = tk.Toplevel(window)
            discription_window.title("Discription")
            discription_window.minsize(800, 600)
            discription_window.resizable(False, False)  # Disable resizing window

            task_name_label = ttk.Label(discription_window, style="main_large.TLabel", text=truncate_string(data[id]["name"], max_length=24))
            task_name_label.place(relx=0.5, rely=0.05, anchor="center")

            discription_label = tk.Text(
                discription_window,
                width=45,
                height=11,
                fg=PALETTE[4],
                bg=PALETTE[2],
                font=(GLOBAL_FONT, GLOBAL_FONT_SIZE_MID),
                relief="flat"
            )
            discription_label.insert(tk.END, discription_text)
            discription_label.config(state="disabled")
            discription_label.place(relx=0.5, rely=0.52, anchor="center")

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
            show_discription_dict = {}  # a dict of show discription buttons
            priority_task_dict = {}  # a dict of priority label
            # iterate through checkboxes
            for i in range(len(data)):
                task = data[i]
                done_var_dict[i] = IntVar(value=data[i]["done"])
                
                if data[i]["done"] == 1:
                    task_label = ttk.Label(window, style="main_strike_mid.TLabel", text=f"{i+1}. {truncate_string(task["name"])}  ")
                else:
                    task_label = ttk.Label(window, style="main_mid.TLabel", text=f"{i+1}. {truncate_string(task["name"])}  ")

                task_label_dict[i] = task_label
                task_label.place(relx=0.01, rely=0.075 * (i+2.8), anchor="w")

                task_checkbox = ttk.Checkbutton(window, variable=done_var_dict[i], takefocus=False, command=lambda i=i: update_task(i))
                check_label_dict[i] = task_checkbox
                task_checkbox.place(relx=0.5, rely=0.075 * (i+2.8), anchor="center")

                if task["discription"] != "":

                    show_discription_btn = tk.Button(
                        window,
                        command=lambda i=i:show_discription(i),
                        font=UNDERLINE_FONT,
                        fg=COLOR["low_priority"],
                        text="Show discription",
                        relief="flat"

                    )
                    show_discription_dict[i] = show_discription_btn 
                    show_discription_btn.place(relx=0.63, rely=0.075 * (i+2.8), anchor="center")

                else:
                    show_discription_dict[i] = None

                priority_task_label = ttk.Label(window)
                if data[i]["priority"] == 0:  # Low priority
                    priority_task_label.configure(style="low_priority.TLabel", text="0")
                elif data[i]["priority"] == 1:  # Middle priority
                    priority_task_label.configure(style="mid_priority.TLabel", text="!")
                else:  # High priority
                    priority_task_label.configure(style="high_priority.TLabel", text="!!")
                priority_task_dict[i] = priority_task_label
                priority_task_label.place(relx=0.9, rely=0.075 * (i+2.8), anchor="center")
                
                delete_task_btn = tk.Button(window,
                                command=lambda i=i: confirm_delete(i),
                                fg=COLOR["error"],
                                font=(GLOBAL_FONT, GLOBAL_FONT_SIZE),
                                relief='flat',
                                text='✕'
                                ) 
                delete_task_dict[i] = delete_task_btn
                delete_task_btn.place(relx=0.95, rely=0.075 * (i+2.8), anchor="center")

        # if reaches task limit

        # ====================================================================================================
        # This annoying limit exists because tkinter is annoying and adding a scrollbar is annoying in tkinter
        # ====================================================================================================
        
        TASK_LIMIT = 11
        if len(task_label_dict) == TASK_LIMIT:
            add_task_btn.configure(state="disabled")
            limit_reached_label = ttk.Label(window, style="error_small.TLabel", text="(You reached the task limit)")
            limit_reached_label.place(relx=0.8, rely= 0.1, anchor="center")
    
    if is_first_time: first_time()
    else: display_tasks()
    
    window.mainloop()

if __name__ == "__main__":
    main()