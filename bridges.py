import numpy as np
import matplotlib.pyplot as plt
from road import Road


class Bridges(object):

    def __init__(self, nrOfSimulations, timeStep, addCarIntervals, simLength):
        self.nrOfSimulations = nrOfSimulations
        self.timeStep = timeStep
        self.simLength = simLength
        self.addCarIntervals = addCarIntervals
        self.simulations = np.zeros(self.nrOfSimulations, dtype = object)
        self.averageSpeeds0 = np.zeros(self.nrOfSimulations)
        self.averageSpeeds1 = np.zeros(self.nrOfSimulations)
        self.averageCarsOnBridge = np.zeros(self.nrOfSimulations)

    def setup(self):
        for i in range(self.nrOfSimulations):
            self.simulations[i] = Road(self.timeStep, self.simLength, self.addCarIntervals[i])

    def simulate(self):
        for i in range(self.nrOfSimulations):
            self.simulations[i].drive()

    def getAverageSpeeds(self):
        index = 0
        for simulation in self.simulations:
            sum0 = 0
            count0 = 0
            sum1 = 0
            count1 = 0
            for speed in simulation.averageSpeedsLane0:
                sum0 += speed
                count0 += 1
            for speed in simulation.averageSpeedsLane1:
                sum1 += speed
                count1 += 1
            self.averageSpeeds0[index]=(float(sum0)/float(count0))*2.2369362920544
            self.averageSpeeds1[index]=(float(sum1)/float(count1))*2.2369362920544
            index+=1

    def getAverageCarsOnBridge(self):
        index = 0
        for simulation in self.simulations:
            sum = 0
            count = 0
            for cars in simulation.carsOnRoadAtTime:
                sum += cars
                count += 1
            self.averageCarsOnBridge[index] = float(sum)/float(count)
            index += 1


A = Bridges(3,1,[2,3,4],500)

A.setup()
A.simulate()
A.getAverageSpeeds()
A.getAverageCarsOnBridge()
print(A.averageSpeeds0)
print(A.averageSpeeds1)
print(A.averageCarsOnBridge)
