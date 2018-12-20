import numpy as np
from car import Car



class Road(object):

    def __init__(self,timeStep):
        self.cars = np.zeros(10, dtype = object)
        self.timeStep = timeStep
        self.carsOnRoad = 0

    def addCar(self):
        self.cars[self.carsOnRoad] = Car()
        self.carsOnRoad +=1

    def removeCar(self, index):
        self.cars = np.delete(self.cars, index)
        self.carsOnRoad -=1

    def updatePositions(self):
        for car in self.cars:
            if isinstance(car,int)!=True:
                car.previousPosition = car.position
                car.position = car.position + car.currentSpeed*self.timeStep

    def nearestCar(self, currentCar):
        minDistance = 1000
        for car in self.cars:
            if isinstance(car,int)!=True:
                if car.position - currentCar.position !=0:
                    if car.lane == currentCar.lane:
                        if car.position - currentCar.position<minDistance and car.position - currentCar.position>0:
                            minDistance = car.position - currentCar.position
        return float(minDistance)/currentCar.currentSpeed



A=Road(1)
A.addCar()

print(A.cars[0].position)
A.updatePositions()
A.addCar()
print(A.cars[0].position)
A.updatePositions()
print(A.cars[0].position)
print(A.cars[1].position)
print(A.nearestCar(A.cars[1]))
