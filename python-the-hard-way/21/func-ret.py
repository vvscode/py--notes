def add(a, b):
    print(f"Adding {a} + {b}")
    return a + b


def subtract(a, b):
    print(f"Subtract {a} - {b}")
    return a - b


def multiply(a, b):
    print(f"multiply {a}*{b}")
    return a * b


def divide(a, b):
    print(f"Devide {a} / {b}")
    return a / b


age = add(30, 5)
height = subtract(200, 14)
weight = multiply(10, 11)
iq = divide(100, 2)

print(f"""
Age: {age}
H: {height}
W: {weight}
IQ: {iq}
""")
