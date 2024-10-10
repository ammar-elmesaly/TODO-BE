# TODO-BE
This is a TODO computer application, it is a CS50 Final Project.
#### Video Demo: [Here](https://www.youtube.com/)

---

#### Description:
##### Brief introduction:
This app is simply a todo list little manager that is powered entirely by python.
It uses the tkinter library which is a famous python library for making GUI Apps.
The tkinter library is slightly out-dated, it is easy to set off but a bit challenging to implement "modern" style in apps.
Feel free to look at the app code, possibly making a PR? It's totally up to you!
##### About the app:
First you may notice this app contains 3 files:
- app.py
- requirements.txt
- .gitignore
<br>
app.py is the main file for the app, .gitignore is the file which contains the files I want to ignore when commiting changes to git. The requirements file contains all the packages that must be installed to run this app. Let's talk about app.py (the main file).

##### app.py
This is a python tkinter app. It uses tkinter's grid system as well as relative positioning system.
It uses 2 constants for storing colors for this app. It uses colors from bootstrap, a popular web framework.
As you go into the main function, first you notice is_first_time, which basically checks if there are no tasks stored in the "database" (which are stored in a json file). A SQL database could've been used, but I used json in this case for convience. 
