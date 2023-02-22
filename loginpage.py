import tkinter as tk
from PIL import ImageTk, Image

root = tk.Tk()
root.title('TED Building Co.')

# set up for the background and picture
canvas = tk.Canvas(root, width = 1900, height = 1100, bg = '#808080' )
canvas.pack()
image = Image.open('logo.png')
image = image.resize((200, 200), Image.ANTIALIAS)
image = ImageTk.PhotoImage(image)
canvas.create_image(635, 300, image = image)

# input boxes
usernameInput = tk.Entry(root, text = 'Username', font = ('Verdana', 14))
canvas.create_window(635, 415, window = usernameInput)

passwordInput = tk.Entry(root, font = ('Verdana', 14))
canvas.create_window(635, 450, window = passwordInput)

# function which takes the user input from the entry boxes
def submitInfo():
    login = False
    global level
    level = 'NULL'
    userName = usernameInput.get()
    userPassword = passwordInput.get()
    # to compare to database
    import databaseMaker
    check = databaseMaker.checkUsers(userName, userPassword)
    # checks if the infomation checks out
    if check != True:
        usernameInput.delete(0, 'end')
        passwordInput.delete(0, 'end')
        wrongPassword = tk.Label(root, text = "Incorrect username/password", bg = '#808080', font = ('Verdana', 14), fg = '#E23232') 
        canvas.create_window(635, 510, window = wrongPassword)
    else:
        # if the information is correct, it checks the level of the user and assigns the correct choices
        level = databaseMaker.checkLevel(userName)
        if level == [('a',)] or level == [('o',)]:
            import adminpage
            WorkerID = databaseMaker.getID(userName)
            print(WorkerID)
            adminpage.adminPage(WorkerID)
        elif level == [('w',)]:
            import WorkInfoPage
            WorkInfoPage.WorkerInfoPage(userName)

# input button
submitData = tk.Button(root, text="->", command=submitInfo)
canvas.create_window(775, 450, window = submitData)
    
def addNewUser():
    import newuser
    newuser.AddNewUser()
    
# new user button, links to seperate file to run that script
newUsers = False
newUser = tk.Button(root, text="New User?", command = addNewUser)
canvas.create_window(635, 485, window = newUser)

root.mainloop()
    
    

