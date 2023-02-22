def WorkerInfoPage(username):

    import tkinter as tk
    import databaseMaker

    currentTask = databaseMaker.getTask(username)
    currentTask = currentTask[0]
    
    # checks if the worker has any tasks assigned to them
    if currentTask[0] == 'NoName':
        labelText = "You don't have any tasks assigned at the moment."

        root = tk.Tk()

        canvas = tk.Canvas(root, width = 500, height = 500, bg = '#808080')
        canvas.pack()

        taskName = tk.Label(root, text = labelText, bg = '#808080', font = ('Verdana', 12))
        canvas.create_window(250, 200, window = taskName)

        root.mainloop()
    else:
        labelText = 'Your current task is: {0}'.format(currentTask[0])

        root = tk.Tk()

        canvas = tk.Canvas(root, width = 500, height = 500, bg = '#808080')
        canvas.pack()

        # prints the current task for the worker
        taskName = tk.Label(root, text = labelText, bg = '#808080', font = ('Verdana', 14))
        canvas.create_window(150, 200, window = taskName)

        def changeTask(username, currentTask, button):
            print(currentTask)
            import databaseMaker
            # removes the displayed task from the TaskID and schedule columns
            databaseMaker.removeCompletedTask(username, currentTask)
            empty = databaseMaker.scheduleCheck(username)
            if empty == True:
                emptyTask = tk.Label(root, text = "You've finished all of your assigned tasks. Well done.", bg = '#808080', font = ('Verdana', 12))
                canvas.create_window(250, 200, window = emptyTask)

                # runs a check to see if the whole project is finished after the completion of this task
                databaseMaker.projectCheck(username)
                button.destroy()
            else:
                # retrieves the next task to be completed
                currentTask = databaseMaker.getTask(username)
                currentTask = currentTask[0]
                taskName = tk.Label(root, text = 'Your current task is: {0}'.format(currentTask[0]), bg = '#808080', font = ('Verdana', 14))
                canvas.create_window(150, 200, window = taskName)
                button.destroy()

                # redefines the button so that new values can be passed into the subroutine
                continueButton = tk.Button(root, text = 'Task Complete', command = lambda: changeTask(username, currentTask[0], continueButton))
                canvas.create_window(150, 250, window = continueButton)

        continueButton = tk.Button(root, text = 'Task Complete', command = lambda: changeTask(username, currentTask[0], continueButton))
        canvas.create_window(150, 250, window = continueButton)

        root.mainloop()

#WorkerInfoPage('w.harrison')

                         
    
