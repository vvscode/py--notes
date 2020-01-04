normal = False

while not normal:
    h1 = input('Enter h1: ')
    word = 'buy'
    count = h1.count(word)
    try:
        freq = round(count/len(h1.split())*100, 2)
        normal = True
        print(freq, 'Frequency')
    except Exception as error:
        print(error, type(error))
        print('Enter h1 again.')
