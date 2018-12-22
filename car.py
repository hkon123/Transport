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
        self.preferedSpeed = self.speedLimit-self.speedDiff + self.speedDiff*np.random.uniform(0,1)

    def setLaneChangeProb(self):
        self.setLaneChangeProb = np.random.uniform(0.5,1)
