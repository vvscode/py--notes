car = {
    'model': 'MeganCar',
    'year': 2018,
    'make': 'SomeFact'
}

try:
    print('model', car['model'])
    print('year', car['year'])
    print('color', car['color'])
except  Exception as ex:
    print('Oops! Something went wrong: ', repr(ex))
finally:
    print('But it\'s still good')