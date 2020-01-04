from threading import Thread


def worker1(asd):
    while True:
        print('Thread1 working', asd)


thread1 = Thread(target=worker1, args=('aaa', ))
thread1.start()


def worker2():
    while True:
        print('222222222222')


thread2 = Thread(target=worker2)
thread2.start()
