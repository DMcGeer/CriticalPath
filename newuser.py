def AddNewUser():

    import tkinter as tk
    
    root = tk.Tk()
    root.title('TED Building Co.')

    # sets up window
    canvas = tk.Canvas(root, width = 1900, height = 1100, bg = '#808080' )
    canvas.pack()

    newName = tk.Entry(root, text = 'New Name', font = ('Verdana', 14))
    canvas.create_window(925, 325, window = newName)
    newNameLabel = tk.Label(root, text = 'First Name:', bg = '#808080', font = ('Verdana', 12))
    canvas.create_window(725, 325, window = newNameLabel)

    newSurname = tk.Entry(root, text = 'New Surname', font = ('Verdana', 14))
    canvas.create_window(925, 360, window = newSurname)
    newSurnameLabel = tk.Label(root, text = 'Surname:', bg = '#808080', font = ('Verdana', 12))
    canvas.create_window(725, 360, window = newSurnameLabel)

    newPassword = tk.Entry(root, text = 'New Password', font = ('Verdana', 14))
    canvas.create_window(925, 395, window = newPassword)
    newPasswordLabel = tk.Label(root, text = 'New Password:', bg = '#808080', font = ('Verdana', 12))
    canvas.create_window(725, 395, window = newPasswordLabel)

    confirmNewPassword = tk.Entry(root, text = 'Confirm New Password:', font = ('Verdana', 14))
    canvas.create_window(925, 430, window = confirmNewPassword)
    confirmNewPasswordLabel = tk.Label(root, text = 'Confirm New Password:', bg = '#808080', font = ('Verdana', 12))
    canvas.create_window(690, 430, window = confirmNewPasswordLabel)

    accessLevels = ['admin', 'owner', 'worker']
    accessLevelChoice = tk.StringVar()
    accessLevelChoice.set(accessLevels[0])
    accessDropChoice = tk.OptionMenu(root, accessLevelChoice, *accessLevels)
    canvas.create_window(1100, 360, window = accessDropChoice)

    def submitInfo():
        
        firstName = newName.get()
        surname = newSurname.get()
        newLevel = accessLevelChoice.get()
        newUsername = newLevel[0] + '.' + surname.lower()
            
    # if the username already occurs in the database, an error message is sent
    # if the passwords don't match, an error message is sent
        import databaseMaker
        if databaseMaker.checkWorker(firstName, surname) == True:
            errorDouble = tk.Label(root, text = 'This user already exists', bg = '#808080', font = ('Verdana', 14))
            canvas.create_window(930, 475, window = errorDouble)
        else:
            newPass = newPassword.get()
            confirmNewPass = confirmNewPassword.get()
            if newPass != confirmNewPass:
                errorPass = tk.Label(root, text = "The passwords don't match", bg = '#808080', font = ('Verdana', 14))
                canvas.create_window(930, 475, window = errorPass)
            else:
                import re
                if any(chr.isdigit() for chr in newPass) == True and bool(re.match('^[a-zA-Z0-9]*$', newPass)) == False:
                    databaseMaker.addInfo('Users', [databaseMaker.incrementWorkerID(), firstName, surname, newUsername, newPass, newLevel[0], 'True', 0], databaseMaker.incrementWorkerID())
                    addedLabel = tk.Label(root, text = "The new user has been added", bg = '#808080', font = ('Verdana', 12))
                    canvas.create_window(930, 475, window = addedLabel)
                else:
                    noChar = tk.Label(root, text = 'Password must contain a special character and number')
                    canvas.create_window(930, 475, window = noChar)

    # input button
    submitNewData = tk.Button(root, text = '->', command = submitInfo)
    canvas.create_window(1065, 431, window = submitNewData)

    root.mainloop()
AddNewUser()
