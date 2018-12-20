import numpy as np
from car import Car



class Road(object):

    def __init__(self,timeStep):
        self.cars = np.zeros(100, dtype = object)
        self.timeStep = timeStep
        self.carsOnRoad = 0
        self.roadLength = 2512

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
                while True:
                    if self.nearestCar(car)>3:
                        while car.currentSpeed<car.preferedSpeed:
                            car.currentSpeed +=0.1
                    else:
                        while self.nearestCar(car)<3:
                            car.currentSpeed -=0.1
                    break
                car.previousPosition = car.position
                car.position = car.position + car.currentSpeed*self.timeStep
                if car.position >=self.roadLength:
                    self.removeCar(index)
                index+=1


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
        while currentTime<100:
            if currentTime%addCarIntervall == 0 and currentTime!=0:
                self.addCar()
            self.printSpeeds()
            self.updatePositions()
            currentTime+=self.timeStep


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


A=Road(1)
A.addCar()

A.drive(2)
