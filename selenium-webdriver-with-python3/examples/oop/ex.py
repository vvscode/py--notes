class Fruit:
    def __init__(self):
        print('Fruit just have been created')

    def nutrition(self):
        print('Fruit\'s nutrition')
        return self

    def fruit_shape(self):
        print('Fruit\'s shape ...')
        return self

class Apple(Fruit):
    def __init__(self):
        Fruit.__init__(self)
        print('Apple init')

    def nutrition(self):
        print('Apple\'s nutrition')
        return self

    def color(self):
        print('red')
        return self

Fruit().nutrition().fruit_shape();
# Fruit just have been created
# Fruit's nutrition
# Fruit's shape ...

apple = Apple() # Fruit just have been created # Apple init
Fruit.nutrition(apple) # Fruit's nutrition
