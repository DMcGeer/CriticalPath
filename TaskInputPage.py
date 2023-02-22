import tkinter as tk
from tkinter import ttk
import sqlite3
def tasks(project, WorkerID):

    root = tk.Tk()
    root.title('TED Building Co.')

    canvas = tk.Canvas(root, width = 1900, height = 1100, bg = '#808080')
    canvas.pack()

    #prints title
    title = tk.Label(root, text = "Task Input", bg = '#808080', font = ('Verdana', 14))
    canvas.create_window(60, 25, window = title)

    #input task information section
    def printHelp1():
        nameHelp = tk.Label(root, text = "Enter the name of a task that needs to be completed")
        canvas.create_window(75, 100, window = nameHelp)
        

    helpButton = tk.Button(root, text = "Help", command = printHelp1)
    canvas.create_window(250, 100, window = helpButton)

    nameLabel = tk.Label(root, text = "Name:", bg = '#808080')
    canvas.create_window(25, 100, window = nameLabel)
    nameInput = tk.Entry(root, text = 'Name', font = ('Verdana', 14))
    canvas.create_window(200, 100, window = nameInput)

    durationLabel = tk.Label(root, text = "Duration:", bg = '#808080')
    canvas.create_window(30, 135, window = durationLabel)
    durationInput = tk.Entry(root, text = 'Duration', font = ('Verdana', 14))
    canvas.create_window(200, 135, window = durationInput)

    #drop down menu for units of the duration
    timeOptions = ["Hours", "Minutes"]
    variable = tk.StringVar()
    variable.set(timeOptions[0])
    durationDropChoice = tk.OptionMenu(root, variable, *timeOptions)
    canvas.create_window(365, 135, window = durationDropChoice)

    previousLabel = tk.Label(root, text = "Predecessors:", bg = '#808080')
    canvas.create_window(40, 170, window = previousLabel)
    previousInput = tk.Entry(root, text = "Immediate Predecessors", font = ('Verdana', 14))
    canvas.create_window(200, 170, window = previousInput)

    def AddTask():

        # stores the tasks in a list (remember to empty list after submitting)
        tasks = []
        duration = int(durationInput.get())
        units = variable.get()

        #converts all times into hours
        if units != "Hours":
            duration = duration / 60

        import databaseMaker
        count = 0
        num = 0
        previous = previousInput.get()
        for i in range(0, len(previous)):
            if previous[i] == ' ' or previous[i] == ',':
                num += 1
            elif databaseMaker.checkPredecessors(previous[i]) == False:
                count += 1
        print(count)
        if count == (len(previous)-num):
            if previous == '':
                previous = 'NULL'
        # need to access database to assign new incremented taskID
            taskID = databaseMaker.incrementID()
            tasks.append([taskID, nameInput.get(), duration, previous, project])
        else:
            errorLabel = tk.Label(root, text = "The entered predecessor(s) aren't in the database", bg = '#808080', font = ('Verdana', 14))
            canvas.create_window(300, 350, window = errorLabel)

        # need to run addInfo in databaseMaker to actually add the info into the database
        databaseMaker.addInfo("Tasks", tasks, WorkerID)

        # needs to call to reprint the database after update
        OutPutTable()
        nameInput.delete(0, 'end')
        durationInput.delete(0, 'end')
        previousInput.delete(0, 'end')
    
    addTask = tk.Button(root, text = "Add task", command = AddTask)
    canvas.create_window(150, 205, window = addTask)

#display table of information section
    def OutPutTable():

        import databaseMaker
        databaseMaker.connect()
        tree = ttk.Treeview(root, column = ("c1", "c2", "c3", "c4"), show = "headings")
        tree.column("#1", anchor = tk.CENTER)
        tree.heading("#1", text = "Task ID")
        
        tree.column("#2", anchor=tk.CENTER)
        tree.heading("#2", text="Task Name")
        
        tree.column("#3", anchor=tk.CENTER)
        tree.heading("#3", text="Duration")
        
        tree.column("#4", anchor = tk.CENTER)
        tree.heading ("#4", text="Immediate Predecessors")

        canvas.create_window(850, 200, window = tree)
        # need to make a screen that finds current project name for this subroutine
        #databaseMaker.View(tree, currentProject)
        databaseMaker.View(tree, project)

    OutPutTable()

    def SubmitProject():

        import scheduling
        scheduling.makeSchedule(project)
        import overseePage
        overseePage.oversee(WorkerID)
        root.destroy()

    submitProject = tk.Button(root, text = 'Submit Project', command = SubmitProject)
    canvas.create_window(150, 240, window = submitProject)
    root.mainloop()
    
#tasks('new builigs', 6)








