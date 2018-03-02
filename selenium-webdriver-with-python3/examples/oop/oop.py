"""
OOP
"""

s = "this is a string"
a = "one more string"
s.upper()
s.lower()

print(type('s'))  # <class 'str'>
print(type('a'))  # <class 'str'>
print(type([1, 2, 3]))  # <class 'list'>

"""
Class
"""


class Car(object):

    def __init__(self, make, model="550i"):
        self.make = make
        self.model = model


c1 = Car('bmw', 'xxl')
print(c1.make)  # bmw
# print(c1['make']) - won't work
print(c1.model)  # xxl

c2 = Car('benz')
print(c2.make)  # benz
print(c2.model)  # 550i

"""
Class Ext
"""


class CarExt(object):
    wheels = 4

    def __init__(self, make, model):
        self.make = make
        self.model = model

    def info(self):
        print("Make of the car: " + self.make)
        print("Model of the car: " + self.model)


c1 = CarExt('bmw', '550i')
print(c1.make)  # bmw
c1.info()
# Make of the car: bmw
# Model of the car: 550i

c2 = CarExt('benz', 'E350')
print(c2.make)  # benz
c2.info()
# Make of the car: benz
# Model of the car: E350

print(CarExt.wheels)  # 4
print(type(c1)) # <class '__main__.CarExt'>
print(isinstance(c1, CarExt)) # True
