from time import sleep

i = 0

while True:
    print('Запрос на сайт: ', i)
    sleep(1)
    i += 1

    if i >= 10:
        break


# for i in range(10):
#     print('Запрос на сайт: ', i)
#     sleep(1)
