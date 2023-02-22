def addNew(WorkerID):
    print(WorkerID)
    
    # this file should:
        # allow admins to add new clients
            # check the information is valid
        # add the new clients to the database
        # move onto the task input page
        
    import tkinter as tk

    root = tk.Tk()
    root.title('TED Building Co.')

    canvas = tk.Canvas(root, width = 1900, height = 1100, bg = '#808080')
    canvas.pack()

    title = tk.Label(root, text = 'Add new client', bg = '#808080', font = ('Verdana', 14))
    canvas.create_window(80, 25, window = title)

    # to add a new client

    projectLabel = tk.Label(root, text = 'Project Name:', bg = '#808080')
    canvas.create_window(50, 65, window = projectLabel)
    projectInput = tk.Entry(root, font = ('Verdana', 14))
    canvas.create_window(250, 65, window = projectInput)
    
    nameLabel = tk.Label(root, text = 'Client First Name:', bg = '#808080')
    canvas.create_window(60, 100, window = nameLabel)
    nameInput = tk.Entry(root, font = ('Verdana', 14))
    canvas.create_window(250, 100, window = nameInput)

    surnameLabel = tk.Label(root, text = 'Client Surame:', bg = '#808080')
    canvas.create_window(50, 135, window = surnameLabel)
    surnameInput = tk.Entry(root, font = ('Verdana', 14))
    canvas.create_window(250, 135, window = surnameInput)

    phoneLabel = tk.Label(root, text = 'Phone Number:', bg = '#808080')
    canvas.create_window(50, 170, window = phoneLabel)
    phoneInput = tk.Entry(root, font = ('Verdana', 14))
    canvas.create_window(250, 170, window = phoneInput)

    siteLabel = tk.Label(root, text = 'Site Name:', bg = '#808080')
    canvas.create_window(50, 205, window = siteLabel)
    siteInput = tk.Entry(root, font = ('Verdana', 14))
    canvas.create_window(250, 205, window = siteInput)

    def AddClient():
        phone = phoneInput.get()

        # ensures the phone number is the correct length
        if len(phone) != 11:
            error = tk.Label(root, text = 'Phone number is the wrong length', bg = '#808080', fg = '#E23232')
            canvas.create_window(120, 275, window = error)
            phoneInput.delete(0, 'end')

        else:

            # ensures the phone number has no letters/symbols
            if phone.isnumeric() == True:
                import databaseMaker
                clientInfo = [projectInput.get(), nameInput.get(), surnameInput.get(), phoneInput.get(), siteInput.get()]
                check = databaseMaker.checkClient(projectInput.get())

                # ensures the client doesn't already exist
                if check == True:
                    WorkID = WorkerID[0]
                    databaseMaker.addInfo('Clients', clientInfo, str(WorkID[0]))
                    import TaskInputPage
                    project = projectInput.get()
                    TaskInputPage.tasks(project, WorkID)

                else:
                    integrityError = tk.Label(root, text = 'This client already exists', bg = '#808080', fg = '#E23232')
                    canvas.create_window(120, 275, window = integrityError)
                    projectInput.delete(0, 'end')
                    
            else:
                intError = tk.Label(root, text = 'Phone number cannot contain letters', bg = '#808080', fg = '#E23232')
                canvas.create_window(120, 275, window = intError)
                phoneInput.delete(0, 'end')

    addClient = tk.Button(root, text = 'Add Client', command = AddClient)
    canvas.create_window(150, 240, window = addClient)

    root.mainloop()
    
#addNew(1)
    
