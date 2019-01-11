import numpy as np



class Car(object):


    def __init__(self):
        self.speedLimit = 70*0.44704
        self.speedDiff = 10*0.44704
        self.setPreferedSpeed()
        self.currentSpeed = self.preferedSpeed
        self.setLaneChangeProb()
        self.lane = 0
        self.position = 0
        self.previousPosition = 0

    def setPreferedSpeed(self):
        self.preferedSpeed = self.speedLimit-(float(self.speedDiff)/float(2)) + self.speedDiff*np.random.uniform(0,1)

    def setLaneChangeProb(self):
        self.laneChangeProb = np.random.uniform(0.5,1)

    def changeLane(self):
        if np.random.uniform(0,1)>self.laneChangeProb:
            if self.lane == 0:
                self.lane = 1
            else:
                self.lane = 0

    def resetCurrentSpeed(self):
        self.preferedSpeed = self.speedLimit-(float(self.speedDiff)/float(2)) + self.speedDiff*np.random.uniform(0,1)
        self.currentSpeed=self.preferedSpeed
