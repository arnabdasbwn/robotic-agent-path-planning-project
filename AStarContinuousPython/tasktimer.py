from direct.task import Task

def taskTimer(task):
    taskTimer.elapsedTime = globalClock.getDt()
    return Task.cont

taskTimer.elapsedTime = 0
