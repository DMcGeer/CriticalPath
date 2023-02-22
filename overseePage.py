def oversee(WorkerID):

    WorkerID = WorkerID[0]
    # this screen should print all of the graphs that show the scheduling
    import tkinter as tk
    from PIL import ImageTk, Image

    import databaseMaker
    ProjectName = databaseMaker.getGraphName(WorkerID[0])
    ProjectName = ProjectName[0]
    ProjectName = ProjectName[0]

    root = tk.Toplevel()
    root.title('TED Building Co.')

    canvas = tk.Canvas(root, width = 700, height = 600, bg = '#808080')
    canvas.pack()

    image = Image.open(ProjectName+'.png')
    image = image.resize((640, 480), Image.ANTIALIAS)
    image = ImageTk.PhotoImage(image)
    canvas.create_image(350, 300, image = image)

    root.mainloop()

#oversee([(1,)])
    
    
    
