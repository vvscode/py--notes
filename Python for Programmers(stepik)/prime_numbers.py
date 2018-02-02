"""
Do you remember prime numbers? 
2, 3, 5, 7, 11, 13 and so on? 
Find the sum of all primes below two million!
"""
from functools import reduce


def is_prime(number):
    print("Check number {}".format(number))
    for i in range(4, int(number/2) + 1):
        if(number % i == 0):
            return False
    return True


target_range = range(1, 2000000)
filtered_range = filter(lambda x: is_prime(x), target_range)
sum = reduce(lambda x, y: x + y, filtered_range)
print(sum)
