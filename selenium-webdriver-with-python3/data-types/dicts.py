print("""
Data type to store more than one value in one variable name, in terms of key value pairs
Dictionary items are in brackets {} in key:value pairs, separated with "," {'k1':'v1', 'k2':'v2'}
Not sequenced, no indexing -> Mapping
""")

car = {'make': 'bmw', 'model': '550i', 'year': 2016}
print(car)  # {'make': 'bmw', 'model': '550i', 'year': 2016}

d = {}

model = car['model']

print(car['make'])  # bmw
print(model)  # 550i

d['one'] = 1
d['two'] = 2

print(d)  # {'one': 1, 'two': 2}

sum_1 = d['two'] + 8
print(sum_1)  # 10
print(d)  # {'one': 1, 'two': 2}
d['two'] = d['two'] + 8
print(d)  # {'one': 1, 'two': 10}

print("""
Nested Dictionary:
d = {'k1': {'nestk1':'nestvalue1', 'nestk2': 'nestvalue2'}}
d['k1']['nestk1']
""")

cars = {'bmw': {'model': '550i', 'year': 2016}, 'benz': {'model': 'E350', 'year': 2015}}
bmw_year = cars['bmw']['year']
print(bmw_year)  # 2016
print(cars['benz']['model'])  # E350

print("""
Dictionary Methods
""")

car = {'make': 'bmw', 'model': '550i', 'year': 2016}
cars = {'bmw': {'model': '550i', 'year': 2016}, 'benz': {'model': 'E350', 'year': 2015}}

print(car.keys())  # dict_keys(['make', 'model', 'year'])
print(cars.keys())  # dict_keys(['bmw', 'benz'])
print(car.values())  # dict_values(['bmw', '550i', 2016])
print(cars.values())  # dict_values([{'model': '550i', 'year': 2016}, {'model': 'E350', 'year': 2015}])
print(car.items())  # dict_items([('make', 'bmw'), ('model', '550i'), ('year', 2016)])

car_copy = car.copy()
print(car_copy)  # {'make': 'bmw', 'model': '550i', 'year': 2016}

print(car.pop('model'))  # 550i
print(car)  # {'make': 'bmw', 'year': 2016}
