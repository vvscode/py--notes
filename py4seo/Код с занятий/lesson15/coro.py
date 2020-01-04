

def calc():
    history = []
    while True:
        x, y = (yield)
        if x == 'h':
            print(history)
            continue
        result = x + y
        print(result)
        history.append(result)


ca = calc()

print(ca)

ca.__next__()

ca.send((1, 2))

breakpoint()

ca.close()
