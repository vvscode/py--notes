websites = 'google.com'


if type(websites) is str:

    website = websites.upper()
    print(website)

    count = 1000

    if 'COM' in website:
        print('COM COM COM')

        if 'T' in website:
            print('Level 33333')

elif websites == 'facebook.com':
    website = 'AAAAAAAAAAAA!'
    print(website)

    bound = 5000

else:
    print('Not Found!')


count = 100 if 'goo' in websites else 0

if 'goo' in websites:
    count = 100
else:
    count = 0


print(count)
