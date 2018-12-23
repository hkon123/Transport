import numpy as np
from car import Car
import matplotlib.pyplot as plt
import os


class Road(object):

    def __init__(self,timeStep):
        self.cars = np.zeros(1000, dtype = object)
        self.timeStep = timeStep
        self.simLength = 1000
        self.carsOnRoad = 0
        self.roadLength = 2512
        self.averageSpeedsLane0 = np.zeros(self.simLength/self.timeStep)
        self.averageSpeedsLane1 = np.zeros(self.simLength/self.timeStep)
        self.changedLaneUp = 0
        self.changedLaneDown = 0

    def addCar(self):
        self.cars[self.carsOnRoad] = Car()
        self.carsOnRoad +=1

    def removeCar(self, index):
        self.cars = np.delete(self.cars, index)
        self.carsOnRoad -=1

    def updatePositions(self):
        index = 0
        for car in self.cars:
            if isinstance(car,int)!=True:
                car.previousPosition = car.position
                car.position = car.position + car.currentSpeed*self.timeStep
                if car.position >=self.roadLength:
                    self.removeCar(index)
                index+=1


    def changeSpeed(self,bugvar):
        for car in self.cars:
            if isinstance(car,int)!=True:
                cantChange = False
                while True:
                    if self.nearestCar(car)>3:
                        while car.currentSpeed<car.preferedSpeed and self.nearestCar(car)>3:
                            car.currentSpeed +=0.1
                        if cantChange == False and car.lane == 1:
                            minFrontDistance,minBackDistance = self.freeLaneChange(car)
                            if minFrontDistance>=3 and minBackDistance>=3:
                                car.changeLane()
                                self.changedLaneDown +=1
                    else:
                        while self.nearestCar(car)<3:
                            if (cantChange == False and car.lane == 0):
                                minFrontDistance,minBackDistance = self.freeLaneChange(car)
                                if minFrontDistance>=3 and minBackDistance>=3:
                                    car.changeLane()
                                    self.changedLaneUp +=1
                                    cantChange=True
                                else:
                                    cantChange = True

                            else:
                                cantChange = True
                                car.currentSpeed -=0.1
                    break


    def freeLaneChange(self,currentCar):
        minFrontDistance = 1000
        minBackDistance = -1000
        for car in self.cars:
            if isinstance(car,int)!=True:
                if car.lane != currentCar.lane:
                    if car.position - currentCar.position !=0:
                        if car.position - currentCar.position<minFrontDistance and car.position - currentCar.position>0:
                            minFrontDistance = car.position - currentCar.position
                        if car.position - currentCar.position>minBackDistance and car.position - currentCar.position<0:
                            minBackDistance = car.position - currentCar.position
        return float(minFrontDistance)/currentCar.currentSpeed, -1*(float(minBackDistance)/currentCar.currentSpeed)



    def nearestCar(self, currentCar):
        minDistance = 1000
        for car in self.cars:
            if isinstance(car,int)!=True:
                if car.position - currentCar.position !=0:
                    if car.lane == currentCar.lane:
                        if car.position - currentCar.position<minDistance and car.position - currentCar.position>0:
                            minDistance = car.position - currentCar.position
        return float(minDistance)/currentCar.currentSpeed


    def drive(self,addCarIntervall):
        currentTime = 0
        index=0
        progress = 0
        while currentTime<self.simLength:
            if currentTime%addCarIntervall == 0 and currentTime!=0:
                self.addCar()
            #self.printBoth()
            self.averageSpeedsLane0[index], self.averageSpeedsLane1[index] = self.averageSpeed()
            self.changeSpeed(index)
            self.updatePositions()
            currentTime+=self.timeStep
            print(index)
            index+=1
            if progress == 0 or currentTime%(self.simLength/100) == 0:
                self.progressBar(progress)
                progress+=1

    def averageSpeed(self):
        count0 = 0
        sum0 = 0
        count1 = 0
        sum1 = 0
        for car in self.cars:
            if isinstance(car,int)!=True:
                if car.lane == 0:
                    sum0 += car.currentSpeed
                    count0 += 1
                else:
                    sum1 += car.currentSpeed
                    count1 += 1
        if count0>0 and count1>0:
            return float(sum0)/float(count0), float(sum1)/float(count1)
        elif count0>0 and count1 == 0:
            return float(sum0)/float(count0), 0


    def printPositions(self):
        for car in self.cars:
            if isinstance(car,int)!=True:
                print(car.position)
        print("\n \n")

    def printSpeeds(self):
        for car in self.cars:
            if isinstance(car,int)!=True:
                print(car.currentSpeed)
        print("\n \n")

    def printBoth(self):
        for car in self.cars:
            if isinstance(car,int)!=True:
                print("pos: " + str(car.position) + "     speed: " + str(car.currentSpeed) + "         lane: " +str(car.lane))
        print("\n \n")

    def plotAverageSpeedOverTime(self):
        time = np.arange(self.simLength/self.timeStep)
        speeds0 = self.averageSpeedsLane0*2.2369362920544
        speeds1 = self.averageSpeedsLane1*2.2369362920544
        plt.plot(time,speeds0)
        plt.plot(time,speeds1, 'r')
        plt.show()

    def progressBar(self,count):
        os.system("cls")
        print(str(count) + "%")



A=Road(1)
A.addCar()

A.drive(2)
#print(A.averageSpeeds*2.2369362920544)
print(A.changedLaneUp)
print(A.changedLaneDown)
A.plotAverageSpeedOverTime()
