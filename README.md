# TODO-BE
This is a TODO computer application, it is a CS50 Final Project.
#### Video Demo: [Here](https://www.youtube.com/)

---

#### Description:
##### Brief introduction:
This app is simply a to-do list little manager that is powered entirely by Python.
It uses the tkinter library, which is a famous Python library for making GUI apps.
The TKInter library is slightly out-dated; it is easy to set off but a bit challenging to implement "modern" style in apps.
Feel free to look at the app code, possibly making a PR? It's totally up to you!
##### About the app:
First, you may notice this app contains 3 files:
- app.py
- requirements.txt
- .gitignore
<br>
app.py is the main file for the app. gitignore is the file that contains the files I want to ignore when committing changes to git. The requirements file contains all the packages that must be installed to run this app. Let's talk about app.py (the main file).

##### app.py
This is a Python TKinter app. It uses Tkinter's grid system as well as a relative positioning system.
It uses 2 constants for storing colors for this app. It uses colors from Bootstrap, a popular web framework.
As you go into the main function, first you notice is_first_time, which basically checks if there are no tasks stored in the "database" (which are stored in a json file). A SQL database could've been used, but I used JSON in this case for convenience.

The app will automatically create a folder for tasks named "tasks,"  in which a json file will be stored, which will contain all your tasks. So the first couple of lines make sure that the tasks folder and the json file are created.
Then, there is a function to set grid weight automatically in a window. and also you find a function that handles errors in user input (providing no task name or too long task name, no priority, etc.).

Then the create task function, which basically creates a new task and then stores it in the json file; each task could optionally have a description, so it also stores it there. If no description is provided, the description will be set simply to `""` in the json file.

Also about the refresh tasks function, it's whole purpose is to delete all the task widgets in a particular window in order to display updated tasks with added, deleted, or new tasks.

You could choose from three priorities: high, middle, or low. These are stored in the json file (note that they must be provided).

Then tkinter style is configured for each of the different widgets, like labels and entries. This is the best practice to stylize widgets in ttk (themed tkinter), but it doesn't work so well with some widgets like buttons; hence, sometimes style is applied directly to a widget with tk instead of applying it indirectly with ttk.

After that, a function is called `first_time()` if there are no tasks in the json file, and `display_tasks()` if there are tasks to display.

In `display_tasks()` lives a nested function `update_task()`, whose whole purpose is to update the state of a particular task when the checkbox is clicked (done or undone); it also updates the state in the database.

Also, you can see `delete_task(id)` and 'confirm_delete(id),` which manage task deletion. The way I am storing widgets is by making a dict for each widget type. For example, a dict for buttons, labels, etc. And accessing them using the widget ID, which is basically the widget's order from 0 to up.

`edit_task(id)` is used to edit task content from name to description to priority.

And then come the dicts and the for loop, which iterates through all tasks from the json file and displays them. If a task has a description, an additional "Show description" button is shown. There is a task limit in this app. To be precise, (**11**) is the limit. Why is that? Tkinter is a little old, implementing a scrollbar is kind of tricky, and I thought for convenience, the 11 limit is fine.

And that's it! Feel free to give any feedback on this project or any thoughts that you might have. Thanks for reading!
