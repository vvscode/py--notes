from pprint import pprint


domain = input('Введите домен: ')


laptop = {
	'domain': domain,
	'brand': 'Apple',
	'city': 'Kyiv',
	'colors': ['grey', 'white', 'black'],
	'price': 2400,
	'price_yesterday': 2200,
	'shops': [{'name': 'Moyo', 'price': 123213},
              {'name': 'Rozetka', 'price': 1000},
              {'name': 'Comfy', 'price': 0}]
}


pprint(laptop)
