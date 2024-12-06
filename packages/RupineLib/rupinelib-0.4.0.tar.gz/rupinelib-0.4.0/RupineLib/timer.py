from datetime import datetime

class Timer():
    def __init__(self):
        self.runTime = 0
        self.startTime = None
        self.endTime = None
        self.isRunning = False

    def start(self):
        if not self.isRunning:
            self.startTime = datetime.now()
            self.isRunning = True

    def stop(self):
        if self.isRunning:
            self.endTime = datetime.now()
            self.runTime = int((self.endTime - self.startTime).total_seconds() * 1000)
            return self.runTime
        else:
            return None

    def currentTime(self):
        if self.isRunning:
            self.runTime = int((datetime.now() - self.startTime).total_seconds() * 1000)
            return self.runTime
        else:
            return None