cars = ['bmw', 'honda', 'audi']
empty_list = []
print(cars, empty_list) # ['bmw', 'honda', 'audi'] []

x = 'test'
print(list(x)) # ['t', 'e', 's', 't']

print(cars[0]) # bmw

cars[1] = 'volga'
print(cars) #['bmw', 'volga', 'audi']

print(len(cars)) # 3

cars.append('Benz')
print(cars) # ['bmw', 'volga', 'audi', 'Benz']

cars.insert(1, 'jeep')
print(cars) # ['bmw', 'jeep', 'volga', 'audi', 'Benz']

print(cars.index('Benz')) # 4

print(cars.pop()) # Benz
print(cars) # ['bmw', 'jeep', 'volga', 'audi']

cars.remove('jeep')
print(cars) # ['bmw', 'volga', 'audi']

print(cars[1:]) # ['volga', 'audi']

cars.sort()
print(cars) # ['audi', 'bmw', 'volga']