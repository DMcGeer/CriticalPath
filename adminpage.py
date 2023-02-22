def adminPage(WorkerID):
    import tkinter as tk

    root = tk.Tk()
    root.title('TED Building Co.')

    canvas = tk.Canvas(root, width = 1900, height = 1100, bg = '#808080')
    canvas.pack()

    choiceLabel = tk.Label(root, text = 'Which screen would you like to see?', bg = '#808080', font = ('Verdana', 14))
    canvas.create_window(635, 285, window = choiceLabel)

    def Oversee():
        import databaseMaker

        # checks if the user is assigned to a project
        if databaseMaker.checkAdmin(WorkerID) == False:
            errorLabel = tk.Label(root, text = "You don't currently have a project to view", bg = '#808080', font = ('Verdana', 14))
            canvas.create_window(635, 405, window = errorLabel)

        else:
            import overseePage
            overseePage.oversee(WorkerID)

    overseeChoice = tk.Button(root, text = 'General Oversee', command = Oversee)
    canvas.create_window(635, 345, window = overseeChoice)

    def newProject():
        # should also check if the admin already has a project. If so, then they shouldn't be able to add a new project
        import databaseMaker 

        if databaseMaker.checkAdmin(WorkerID) == False:
            import clientPage
            clientPage.addNew(WorkerID)
            
        else:
            errorLabel = tk.Label(root, text = 'You already have an assigned project, so you can only view for now', bg = '#808080', font = ('Verdana', 14))
            canvas.create_window(635, 405, window = errorLabel)

    projectChoice = tk.Button(root, text = 'Add new project', command = newProject)
    canvas.create_window(635, 375, window = projectChoice)

    root.mainloop()


    
#adminPage([(1,)])
