"""
Variable Scope
"""

a = 10


def test_method(a):
    print("Value of local 'a' is: " + str(a)) # Value of local 'a' is: 10
    a = 2
    print("New value of local 'a' is: " + str(a)) # New value of local 'a' is: 2


print("Value of global 'a' is: " + str(a)) # Value of global 'a' is: 10
test_method(a)
print("Did the value of global 'a' change? " + str(a)) # Did the value of global 'a' change? 10

a = 10


def test_method():
    global a
    print("Value of 'a' inside the method is: " + str(a)) # Value of 'a' inside the method is: 10
    a = 2
    print("New value of 'a' inside the method is changed to: " + str(a)) # New value of 'a' inside the method is changed to: 2


print("Value of global a is: " + str(a)) # Value of global a is: 10
test_method()
print("Did the value of global 'a' change? " + str(a)) # Did the value of global 'a' change? 2
