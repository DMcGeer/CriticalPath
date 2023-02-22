import sqlite3

def makeTables():
    con1 = sqlite3.connect("TaskData.db")
    cur1 = con1.cursor()
    cur1.execute("PRAGMA foreign_keys = ON")
    con1.commit()
    # sets up the client table
    cur1.execute("""CREATE TABLE IF NOT EXISTS tblClients(
            ProjectName VARCHAR(20) NOT NULL PRIMARY KEY,
            ClientFirstName VARCHAR(20) NOT NULL,
            ClientSurname VARCHAR(20) NOT NULL,
            PhoneNumber CHAR(11) NOT NULL,
            SiteName VARCHAR(20) NOT NULL, 
            AssignedAdmin INTEGER NOT NULL,
            FOREIGN KEY (AssignedAdmin) REFERENCES tblUsers(WorkerID));
            """)
    con1.commit()
    # sets up the task table
    cur1.execute("""CREATE TABLE IF NOT EXISTS tblTasks(
            TaskID INTEGER NOT NULL PRIMARY KEY,
            TaskName VARCHAR(30) NOT NULL,
            Duration REAL NOT NULL,
            ImmediatePredecessors VARCHAR(16),
            ProjectName VARCHAR(20) NOT NULL, 
            FOREIGN KEY (ProjectName) REFERENCES tblClients(ProjectName))
            """)
    con1.commit() 
    # sets up the user table
    cur1.execute("""CREATE TABLE IF NOT EXISTS tblUsers(
            WorkerID INTEGER NOT NULL PRIMARY KEY,
            FirstName VARCHAR(20) NOT NULL,
            Surname VARCHAR(20) NOT NULL,
            Username VARCHAR(20) NOT NULL,
            Password VARCHAR(20) NOT NULL,
            AccessLevel CHAR(1) NOT NULL,
            Availability BOOLEAN NOT NULL,
            TaskID INTEGER,
            FOREIGN KEY (TaskID) REFERENCES tblTasks(TaskID),
            Schedule VARCHAR(100));
            """)
    con1.commit()

def getGraphName(WorkerID):
    con1 = sqlite3.connect("TaskData.db")
    cur1 = con1.cursor()
    name = cur1.execute("SELECT ProjectName FROM tblClients WHERE tblClients.AssignedAdmin = ?", (str(WorkerID), )).fetchall()
    return name

def checkAdmin(WorkerID):
    print(str(WorkerID))
    worker = WorkerID[0]
    con1 = sqlite3.connect("TaskData.db")
    cur1 = con1.cursor()
    admin = cur1.execute("""SELECT tblClients.ProjectName
        FROM tblClients
        WHERE tblClients.AssignedAdmin = ?""", (str(worker[0]), )).fetchall()
    print(admin)
    if admin != []:
        return True
    else:
        return False

def findAvailable():
    # finds which workers are available
    con1 = sqlite3.connect("TaskData.db")
    cur1 = con1.cursor()
    available = cur1.execute("""SELECT tblUsers.WorkerID
        FROM tblUsers
        WHERE (tblUsers.Availability <> False) AND (tblUsers.AccessLevel = 'w');""").fetchall()
    if len(available) > 5:
        available = available[:5]
    print(available)
    return available

def getID(userName):
    con1 = sqlite3.connect("TaskData.db")
    cur1 = con1.cursor()
    ID = cur1.execute("""SELECT WorkerID
        FROM tblUsers
        WHERE tblUsers.Username = (?)""", (userName, )).fetchall()
    return ID

def findWorkers(ProjectName):
    con1 = sqlite3.connect("TaskData.db")
    cur1 = con1.cursor()
    workers = cur1.execute("""SELECT tblUsers.WorkerID, tblUsers.FirstName, tblUsers.Surname
        FROM tblUsers, tblTasks
        WHERE (tblUsers.AccessLevel = 'w') AND (tblUsers.TaskID = tblTasks.TaskID) AND (tblTasks.ProjectName = ?) AND tblTasks.TaskID <> 0; """, (ProjectName, )).fetchall()
    return workers

def getscheduleTasks(critical, project):
    sqlCritical = critical[0]
    for i in range(1, len(critical)):
        sqlCritical = sqlCritical+', '+critical[i]
        print(sqlCritical)
    con1 = sqlite3.connect("TaskData.db")
    cur1 = con1.cursor()
    tasks = cur1.execute("""SELECT tblTasks.TaskName, tblTasks.Duration 
        FROM tblTasks
        WHERE tblTasks.ProjectName = ? AND tblTasks.TaskName NOT IN (?) AND tblTasks.TaskID <> 0; """, (project, sqlCritical)).fetchall()
    print(tasks)
    return tasks

#getscheduleTasks(['B', 'E', 'G'], 'LU')

def checkCritical(critical, project):
    con1 = sqlite3.connect("TaskData.db")
    cur1 = con1.cursor()
    tasks = cur1.execute("SELECT tblTasks.TaskName, tblTasks.Duration FROM tblTasks WHERE tblTasks.TaskName NOT IN (?, ?, ?) AND tblTasks.TaskID <> 0 AND tblTasks.ProjectName = ?", (critical[0], critical[1], critical[2], project)).fetchall()
    #print(tasks)
    return tasks

#checkCritical(['B', 'E', 'G'], 'LU')

def getState(taskID):
    con1 = sqlite3.connect("TaskData.db")
    cur1 = con1.cursor()
    state = cur1.execute("""SELECT tblTasks.ImmediatePredecessors 
        FROM tblTasks
        WHERE tblTasks.TaskID = ?;""", (taskID, )).fetchall()
    return state

def getSuccessors(taskName):
    con1 = sqlite3.connect("TaskData.db")
    cur1 = con1.cursor()
    successors = cur1.execute("""SELECT TaskName FROM tblTasks WHERE tblTasks.ImmediatePredecessors = ?;""", (taskName, )).fetchall()
    return successors

def checkWorker(first, surname):
    con1 = sqlite3.connect("TaskData.db")
    cur1 = con1.cursor()
    worker = cur1.execute("""SELECT tblUsers.WorkerID FROM tblUsers WHERE tblUsers.FirstName = ? AND tblUsers.Surname = ?;""", (first, surname)).fetchall()
    print(worker)
    if worker != []:
        return True
    else:
        return False

def checkUsers(Username, Password):
        # checks to see if the username and password given are in the database
        con1 = sqlite3.connect("TaskData.db")
        cur1 = con1.cursor()
        # this statement won't pick up anything from the database
        realUser = cur1.execute("""SELECT tblUsers.Password FROM tblUsers WHERE tblUsers.Username = ?;""", (Username, ))
        realUser = realUser.fetchall()
        if realUser == 'NULL':
                return False
        elif realUser == [(Password,)]:
                return True
        else:
                return "Incorrect Password"

def addInfo(Table, Information, WorkerID):
    con1 = sqlite3.connect("TaskData.db")
    cur1 = con1.cursor()
    if Table == "Users":
            cur1.execute("INSERT INTO tblUsers(WorkerID, FirstName, Surname, Username, Password, AccessLevel, Availability, TaskID) VALUES(?, ?, ?, ?, ?, ?, ?, ?)",(Information[0], Information[1], Information[2], Information[3], Information[4], Information[5], Information[6], Information[7]))
            con1.commit()
    elif Table == "Clients":
            cur1.execute("INSERT INTO tblClients(ProjectName, ClientFirstName, ClientSurname, PhoneNumber, SiteName, AssignedAdmin) VALUES(?, ?, ?, ?, ?, ?)",(Information[0], Information[1], Information[2], Information[3], Information[4], WorkerID))
            con1.commit()
    elif Table == "Tasks":
            cur1.execute("INSERT INTO tblTasks(TaskID, TaskName, Duration, ImmediatePredecessors, ProjectName) VALUES(?, ?, ?, ?, ?)",(Information[0][0], Information[0][1], Information[0][2], Information[0][3], Information[0][4]))
            con1.commit()

def checkLevel(username):
    con1 = sqlite3.connect("TaskData.db")
    cur1 = con1.cursor()
    level = cur1.execute("SELECT AccessLevel FROM tblUsers WHERE (tblUsers.Username = ?);", (username, )).fetchall()
    return level
    
def connect():
    con1 = sqlite3.connect("TaskData.db")
         
def View(tree, currentProject):
    import tkinter as tk
    con1 = sqlite3.connect("TaskData.db")
    cur1 = con1.cursor()
    cur1.execute("SELECT TaskID, TaskName, Duration, ImmediatePredecessors FROM tblTasks WHERE (tblTasks.ProjectName = ? AND tblTasks.TaskID > 0) ORDER BY TaskID ASC", (currentProject, ))
    rows = cur1.fetchall()    
    for row in rows:
        print(row) 
        tree.insert("", tk.END, values=row)        
    con1.close()

def getTask(username):
    # subroutine to find the corresponding workerID
    con1 = sqlite3.connect("TaskData.db")
    cur1 = con1.cursor()
    currentTask = cur1.execute("SELECT tblTasks.TaskName FROM tblUsers, tblTasks WHERE (tblUsers.Username = ? AND tblUsers.TaskID = tblTasks.TaskID)", (username, )).fetchall()
    return currentTask

def removeCompletedTask(username, currentTask):
    con1 = sqlite3.connect("TaskData.db")
    cur1 = con1.cursor()
    # fetches the schedule of the required worker
    schedule = cur1.execute("SELECT tblUsers.Schedule FROM tblUsers WHERE tblUsers.Username = ?", (username,)).fetchall()
    # removes the first element of the list
    schedule = schedule[0]
    task = currentTask[0]
    newSchedule = schedule[0].replace(', ', '', 1)
    newSchedule = newSchedule.replace(task, '', 1)
    print(newSchedule)
    # overwrites the current schedule with the new one
    if newSchedule != '':
        newTaskID = findTaskID(newSchedule[0])
        newTaskID = newTaskID[0]
        print(newTaskID[0])
    else:
        newSchedule = 'NULL'
        newTaskID = [0]
    cur1.execute("""UPDATE tblUsers SET Availability = 'True', Schedule = ?, TaskID = ? WHERE Username = ?""", (newSchedule, newTaskID[0], username))
    con1.commit()

def scheduleCheck(username):
    con1 = sqlite3.connect("TaskData.db")
    cur1 = con1.cursor()
    schedule = cur1.execute("SELECT tblUsers.Schedule FROM tblUsers WHERE tblUsers.Username = ?", (username,)).fetchall()
    print(schedule)
    if schedule == [('NULL',)]:
        return True
    else:
        return False

def getProject(username):
    con1 = sqlite3.connect("TaskData.db")
    cur1 = con1.cursor()
    projectName = cur1.execute("SELECT tblTasks.ProjectName FROM tblUsers, tblTasks WHERE tblUsers.Username = ? AND tblUsers.TaskID = tblTasks.TaskID", (username, )).fetchall()
    return projectName

def projectCheck(username):
    con1 = sqlite3.connect("TaskData.db")
    cur1 = con1.cursor()
    projectName = getProject(username)
    projectName = projectName[0]
    check = cur1.execute("SELECT tblUsers.Schedule FROM tblUsers, tblTasks WHERE tblTasks.ProjectName = ? AND tblUsers.TaskID = tblTasks.TaskID", (projectName[0], )).fetchall()
    if check == [('NULL',)]:
        cur1.execute("UPDATE tblClients SET AssignedAdmin = NULL WHERE tblClients.ProjectName = ?", (projectName, ))
        con1.commit()

def incrementID():
    # subroutine to find what the next ID should be for a new task
    con1 = sqlite3.connect("TaskData.db")
    cur1 = con1.cursor()
    taskID = cur1.execute("SELECT MAX(TaskID) FROM tblTasks").fetchall()
    for i in range(0, 100):
        if [(i,)] == taskID: 
            newID = i + 1
    return newID

def incrementWorkerID():
    con1 = sqlite3.connect("TaskData.db")
    cur1 = con1.cursor()
    workerID = cur1.execute("SELECT MAX(WorkerID) FROM tblUsers").fetchall()
    for i in range(0, 100):
        if[(i,)] == workerID:
            newID = i + 1
    print(newID)
    return newID

def clearTable():
    con1= sqlite3.connect("TaskData.db")
    cur1 = con1.cursor()
    cur1.execute("DROP TABLE IF EXISTS tblTasks")
    con1.commit()
    makeTables()

def getRelevant(currentProject):
    con1 = sqlite3.connect("TaskData.db")
    cur1 = con1.cursor()
    relevant = cur1.execute("SELECT TaskID, TaskName, Duration, ImmediatePredecessors FROM tblTasks WHERE ProjectName = ? AND TaskID > 0 ORDER BY TaskID ASC", (currentProject,)).fetchall()
    return relevant

def getDuration(taskName):
    con1 = sqlite3.connect("TaskData.db")
    cur1 = con1.cursor()
    statement = "SELECT Duration FROM tblTasks WHERE TaskName = '{0}'".format(taskName)
    duration = cur1.execute(statement).fetchall()
    return duration

def findTaskID(taskName):
    con1 = sqlite3.connect("TaskData.db")
    cur1 = con1.cursor()
    taskID = cur1.execute("SELECT tblTasks.TaskID FROM tblTasks WHERE TaskName = ?", (taskName, )).fetchall()
    return taskID

def setAvailable(workerID, taskName, schedule):
    con1 = sqlite3.connect("TaskData.db")
    cur1 = con1.cursor()
    taskID = findTaskID(taskName)
    taskID = taskID[0]
    cur1.execute("""UPDATE tblUsers SET Availability = 'False', TaskID = ?, Schedule = ? WHERE WorkerID = ?""", (taskID[0], schedule, workerID))
    con1.commit()

def addColumn():
    con1 = sqlite3.connect("TaskData.db")
    cur1 = con1.cursor()
    cur1.execute("ALTER TABLE tblUsers ADD COLUMN Schedule VARCHAR(100)")

def checkClient(project):
    con1 = sqlite3.connect("TaskData.db")
    cur1 = con1.cursor()
    check = cur1.execute("SELECT ProjectName FROM tblClients WHERE ProjectName = ?", (project,)).fetchall()
    if check != []:
        return False
    else:
        return True

def checkPredecessors(previous):
    con1 = sqlite3.connect("TaskData.db")
    cur1 = con1.cursor()
    check = cur1.execute("SELECT TaskName FROM tblTasks WHERE TaskName = ?;", (previous, )).fetchall()
    if check != []:
        return True
    else:
        return False
#addColumn()