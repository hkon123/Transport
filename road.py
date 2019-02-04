import numpy as np
from car import Car
import matplotlib.pyplot as plt
import os
import time


class Road(object):

    def __init__(self,simLength,addCarIntervall, roadLength = 2512, minSepperation = 3, currentSim =1, totalSims =1):
        self.cars = np.zeros(1800, dtype = object)
        #self.timeStep = timeStep
        self.simLength = simLength
        self.minSepperation = minSepperation
        self.addCarIntervall = addCarIntervall
        print(self.addCarIntervall)
        self.timeStep, self.interval = self.setTimeStep()
        self.carsOnRoad = 0
        self.roadLength = roadLength
        self.averageSpeedsLane0 = np.zeros(int(self.simLength/self.timeStep)+2)
        self.averageSpeedsLane1 = np.zeros(int(self.simLength/self.timeStep)+2)
        self.changedLaneUp = 0
        self.changedLaneDown = 0
        self.carsOnRoadAtTime = np.zeros(int(self.simLength/self.timeStep)+2)
        self.carsNotAdded = 0
        self.currentSim = currentSim
        self.totalSims = totalSims

    def setTimeStep(self):
        if isinstance(self.addCarIntervall,int) == True or self.addCarIntervall ==2 or self.addCarIntervall ==3 or self.addCarIntervall == 4 or self.addCarIntervall == 5:
            return 1, self.addCarIntervall
        elif self.addCarIntervall==1:
            return 0.5, 2
        elif self.addCarIntervall<1:
            return self.addCarIntervall/float(2), 2
        elif self.addCarIntervall>1 and self.addCarIntervall<2:
            return self.addCarIntervall/float(2), 2
        elif self.addCarIntervall>2 and self.addCarIntervall<3:
            return self.addCarIntervall/float(3), 3
        elif self.addCarIntervall>3:
            return self.addCarIntervall/float(4), 4

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
        index = 0
        for car in self.cars:
            if isinstance(car,int)!=True:
                cantChange = False
                if self.nearestCar(car)>self.minSepperation:
                    while car.currentSpeed<car.preferedSpeed and self.nearestCar(car)>self.minSepperation:
                        car.currentSpeed +=0.1
                    if cantChange == False and car.lane == 1:
                        minFrontDistance,minBackDistance = self.freeLaneChange(car)
                        if minFrontDistance>=self.minSepperation and minBackDistance>=self.minSepperation:
                            car.changeLane()
                            self.changedLaneDown +=1
                else:
                    while self.nearestCar(car)<self.minSepperation:
                        if cantChange == False and car.lane == 0:
                            minFrontDistance,minBackDistance = self.freeLaneChange(car)
                            if minFrontDistance>=self.minSepperation and minBackDistance>=self.minSepperation:
                                car.changeLane()
                                self.changedLaneUp +=1
                                cantChange=True
                            else:
                                cantChange = True

                        else:
                            #print(str(bugvar) +"  " + str(self.nearestCar(car)) + "  " + str(self.minSepperation))
                            cantChange = True
                            car.currentSpeed -=0.01
                            if car.currentSpeed<0:
                                #print(car.currentSpeed)
                                #print(car.position)
                                #car.resetCurrentSpeed()
                                #print(self.nearestCar(car))
                                #self.printBoth()
                                self.removeCar(index)
                                self.carsNotAdded +=1
                                #time.sleep(10)
                                break
            index +=1

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


    def drive(self,):
        currentTime = 0
        index=0
        progress = 0
        while currentTime<self.simLength:
            if index%self.interval == 0 or currentTime==0:
                self.addCar()
            #self.printBoth()
            self.averageSpeedsLane0[index], self.averageSpeedsLane1[index] = self.averageSpeed()
            self.carsOnRoadAtTime[index] = self.carsOnRoadAtTimeSet()
            self.changeSpeed(index)
            self.updatePositions()
            currentTime+=self.timeStep
            #print(index)
            index+=1
            if progress == 0 or int(currentTime)%(self.simLength/100) == 0:
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

    def carsOnRoadAtTimeSet(self):
        return self.carsOnRoad


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
        time = np.arange(0,self.simLength,self.timeStep)
        speeds0 = self.averageSpeedsLane0*2.2369362920544
        speeds1 = self.averageSpeedsLane1*2.2369362920544
        while len(time)<len(speeds0):
            time = np.append(time, time[-1]+self.timeStep)
        plt.plot(time,speeds0, label = 'Slow Lane')
        plt.plot(time,speeds1, 'r', label = 'Fast Lane')
        plt.plot(time,self.carsOnRoadAtTime, 'y', label = 'Total cars on road')
        plt.legend(loc = 'best')
        plt.ylabel("Average speed/number of cars")
        plt.xlabel("Time")
        plt.savefig("Vshort.png")
        plt.show()

    def progressBar(self,count):
        os.system("cls")
        print(str(count) + "%")
        print("simulation: " + str(self.currentSim) + "/" + str(self.totalSims))


'''remove comment to simulate single experiment
A=Road(1800,1.6)



A.drive()
#print(A.averageSpeeds*2.2369362920544)
print(A.timeStep)
print(A.changedLaneUp)
print(A.changedLaneDown)
print(A.carsNotAdded)
A.plotAverageSpeedOverTime()
'''
