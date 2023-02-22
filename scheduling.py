def makeSchedule(ProjectName):

    class Worker():
        
        def __init__(self, ID, totalDuration = 0):
            self.ID = ID
            self.jobList = []
            self.totalDuration = totalDuration

        def addTasks(self, job, duration, earlyTime, lateTime, float):
            # should check what the worker is last doing
            current = self.getTime()
            # if the early time of the task is greater than the totalDuration, it should be added
            if earlyTime >= current:
                self.jobList.append([job, earlyTime, duration])
                self.totalDuration += duration

            else:
                # if not, 1 should be added from the float until the two values are equal, and add the task at that point + duration
                count = 0
                for i in range(0, float):
                    earlyTime += 1
                    if earlyTime >= current:
                        self.jobList.append([job,earlyTime, duration])
                        self.totalDuration += (duration)
                        count += 1
                        break

                if count == 0:
                    return False
            
        # passes in self, critical[0], critical[1]
        def addCriticalTasks(self, taskName, duration):
            tasksToBeAdded = []
            # after this loop, the job list should look like: [[TaskName, duration], [TaskName, duration]]
            for i in range(0, len(taskName)):
                import databaseMaker
                taskDuration = databaseMaker.getDuration(taskName[i])
                if i == 0:
                    totalEarly = 0

                else:
                    earlyTime = databaseMaker.getDuration(taskName[i-1])
                    for j in range(0, len(earlyTime)):
                        early = earlyTime[j]
                    early = early[0]
                    for k in range(0, len(taskName)):
                        totalEarly = early + tasksToBeAdded[-1][1]

                tasksToBeAdded.append([taskName[i], totalEarly, taskDuration[0][0]])
            self.jobList = tasksToBeAdded
            self.totalDuration = duration

        def getJobs(self):
            return self.jobList

        def addLaterTasks(self, TaskName, duration):
            # should add the task onto the end of joblist and add duration
            self.jobList.append([TaskName, self.totalDuration, duration])
            self.totalDuration += duration

        def getTime(self):
            return self.totalDuration

        def checkAvailable(self, lateTime):
            # if the total duration (the tasks they are already set to complete) is larger than the early time + float, then the worker is unavailable
            if self.totalDuration > lateTime:
                return False
            else:
                return True 
   
    import databaseMaker
    tasks = databaseMaker.getRelevant(ProjectName)
    print(tasks)

    # assigns early times
    early = [0]*len(tasks)
    total = []

    # repeats for each task
    for i in range(0, len(tasks)):
        ES = []
        before = databaseMaker.getState(tasks[i][0])
        # the default early time should only be changed if the task has predecessors 
        if before != [('NULL',)]:

            # repeats for every predecessor the task has
            for j in range(0, len(before)):

                # searches for the early time of the predecessor
                for k in range(0, len(early)):

                    # finds the index of the predecessor
                    if (tasks[k][1],) == before[j]:

                        # once found, it sets the possible early time to the previous early time + duration of current task
                        ES.append(early[k] + tasks[k][2])
                        
            early[i] = max(ES)
        total.append(early[i]+tasks[i][2])
    
    # defines the critical time
    maximum = max(total)

    # assigns late times 
    late = [0]*len(tasks)

    # repeats for each task (backwards)
    for i in range(len(tasks)-1, -1, -1):

        LF = []
        after = databaseMaker.getSuccessors(tasks[i][1])
        if after == []:

            # if no tasks happen after, it's late time will be the same as the duration of the critical path
            late[i] = maximum

        else:

            # searches for each successor
            for j in range(0, len(after)):

                # finds the index of the successor
                for k in range(0, len(late)):

                    if (tasks[k][1],) == after[j]:

                        # once found, the late time = late time of successor - duration of successor
                        LF.append(late[k] - tasks[k][2])

            late[i] = min(LF)

    # to find the critical path
    criticalTasks = []
    for i in range (0, len(tasks)):
        if early[i] == late[i] - tasks[i][2]:
            criticalTasks.append(tasks[i][1])
    critical = (criticalTasks, maximum)
    print(critical)

    # removes the critical activities from the graph's information
    num = 0
    for i in range(0, len(tasks)):

        if tasks[i][1] in critical[0]:

            del early[i-num]
            del late[i-num]
            num += 1

    # imports the workers that are available, but limits it to 5 
    import databaseMaker
    availableWorkers = databaseMaker.findAvailable()

    # should calculate the minimum number of workers needed and reduce the number of workers to that

    sumOfTasks = 0
    for i in range(0, len(tasks)):
        sumOfTasks += tasks[i][2]
    lowerBound = sumOfTasks / critical[1]
    import math
    lowerBound = math.ceil(lowerBound)
    availableWorkers = availableWorkers[:lowerBound]


    workers = []
    count = 0
    
    # instantiates an object for each worker's existence
    for i in range(0, len(availableWorkers)):
        worker = Worker(availableWorkers[i][0])
        workers.append(worker)
        count += 1
        if count == 1:
            workers[i].addCriticalTasks(critical[0], critical[1])

    import databaseMaker
    #scheduleTasks = databaseMaker.getscheduleTasks(critical[0], ProjectName)
    scheduleTasks = databaseMaker.checkCritical(critical[0], ProjectName)
   
    # sorts tasks by early times (bubble sort for ease)
    for i in range(len(early)):

        for j in range(0, len(early)-i-1):

            if early[j] > early[j+1]:
                early[j], early[j+1] = early[j+1], early[j]
                late[j], late[j+1] = late[j+1], late[j]
                scheduleTasks[j], scheduleTasks[j+1] = scheduleTasks[j+1], scheduleTasks[j]
    print(early)
    print(scheduleTasks)
    floats = []
    # finds the float
    # the float = late - early - duration
    for i in range(0, len(scheduleTasks)):

        float = late[i]-early[i]
        float = float - scheduleTasks[i][1]
        floats.append(float)

    # assigns the task if the worker is available within their early time + float
    for i in range (0, len(scheduleTasks)):
        
        # checks which workers are available
        workerNo = 0
        count = 0
        done = False
        # while the task hasn't been added and there are workers left to check
        while workerNo <= len(workers) and done == False:

            if workers[workerNo].checkAvailable(early[i]+floats[i]) == True:
                # passes in (taskName, duration, early time, late time, float)
                addTask = workers[workerNo].addTasks(scheduleTasks[i][0], scheduleTasks[i][1], early[i], late[i], floats[i])
                done = True

            else:
                count += 1
            workerNo += 1
        # if the task hasn't been added within the float, it should be added to the worker with the smallest total duration
        if count >= len(workers):

            Duration = []
            for k in range(0, len(workers)):

                Duration.append(workers[k].totalDuration)
                if workers[k].totalDuration <= min(Duration):
                    temp = workers[k]
            temp.addLaterTasks(scheduleTasks[i][0], scheduleTasks[i][1])
    
    returnable = []
    for i in range(0, len(workers)):
        # should be in the structure:[workerID, [[TaskName, start, duration], [TaskName, start, duration]]]
        returnable.append([workers[i].ID, workers[i].jobList])
    print(returnable)

    # need to assign the first taskID to the worker in database (for worker info page)
    import databaseMaker
    for i in range(0, len(workers)):
        schedule = returnable[i][1][0][0]
        for j in range (1, len(returnable[i][1])):
            # adds the tasks to the schedule, using recursion
            schedule = schedule + ', ' + returnable[i][1][j][0]
        databaseMaker.setAvailable(workers[i].ID, returnable[i][1][0][0], str(schedule))

    # plots the graph
    import graphMaker
    graphMaker.graphMaker(returnable, critical, ProjectName)

#import databaseMaker
#relevant = databaseMaker.getRelevant('LU')
makeSchedule('LU')