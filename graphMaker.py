# this file should
#     1. import the workers that are on this project
#     2. plot the graph based on the start schedule time and duration of the tasks

def graphMaker(schedule, critical, ProjectName):
    import matplotlib.pyplot as plt
    fig, chart1 = plt.subplots()
    chart1.set_ylim(0, 25)
    # the maximum value to graph can show is the length of the critical path
    chart1.set_xlim(0, critical[1])

    import databaseMaker 
    workers = databaseMaker.findWorkers(ProjectName)
    
    # should set y ticks for the amount of workers
    params = []
    for i in range(0, len(workers)):
        params.append((10*(i+1)))
    chart1.set_yticks(params)


    # should set y labels for the IDs of the workers
    workersList = []
    for i in range(0, len(workers)):
        workersList.append(workers[i][2])
    workersList.reverse()
    chart1.set_yticklabels(workersList)

    chart1.grid(True)

    # should define the bars based on the start times and duration of each task
    for i in range (0, len(workersList)):
        earlyAndDuration = []

        tabColours = ['tab:red', 'tab:blue', 'tab:green', 'tab:orange', 'tab:purple']
        usedTabColours = []

        for u in range(0, len(schedule[i][1])):

            # should make a tape to make each task a different colour
            usedTabColours.append(tabColours[u%5])

            # should make a list of the early times and duration of each task per worker
            earlyAndDuration.append(schedule[i][1][u][1:])

            # should pass in (text, (coordinates), fontsize)
            print(schedule[i][1][u][0])
            chart1.annotate(schedule[i][1][u][0], (schedule[i][1][u][1],(i+1)*9), fontsize = 11)

        earlyAndDuration = tuple(earlyAndDuration)
        
        # should be set out ([(task 1, duration), (task2, duration)...], (height above 0 on y axis, height of bar), colour of bar )

        print(earlyAndDuration)
        chart1.broken_barh(earlyAndDuration, ((i+1)*8, 4), facecolors = tuple(usedTabColours))

    plt.savefig(ProjectName+'.png')

graphMaker([[3, [['B', 0, 7], ['E', 7, 6], ['G', 13, 10]]], [4, [['A', 0, 5], ['C', 5, 1], ['I', 6, 3], ['D', 9, 2], ['F', 11, 1], ['J', 12, 4], ['H', 16, 7]]]], (['G', 'E', 'B'], 23), 'LU')