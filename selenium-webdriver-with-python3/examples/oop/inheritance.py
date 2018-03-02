class Car(object):

    def __init__(self):
        print("You just created the car instance")

    def drive(self):
        print("Car started...")

    def stop(self):
        print("Car stopped")


class BMW(Car):

    def __init__(self):
        Car.__init__(self)
        print("You just created the BMW instance")

class Audi(Car):
    def __init__(self):
        Car.__init__(self)
        print("You just created the Audi instance")

    def drive(self):
        super(Audi, self).drive()
        print("You are driving a Audi, Enjoy...")

    def headsup_display(self):
        print("This is a unique feature")

c = Car()  # You just created the car instance
c.drive()  # Car started...
c.stop()  # Car stopped

b = BMW()
# You just created the car instance
# You just created the BMW instance
b.drive()  # Car started...
b.stop()  # Car stopped
print(isinstance(b, Car))  # True


a = Audi()
# You just created the car instance
# You just created the Audi instance
a.drive()
# Car started...
# You are driving a Audi, Enjoy...
a.stop() # Car stopped
a.headsup_display() # This is a unique feature