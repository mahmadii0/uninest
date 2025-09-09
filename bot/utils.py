import random

def rand(randnums):
    num = random.randint(10 ** 7, 10 ** 8 - 1)
    if num in randnums:
        return rand(randnums)
    else:
        return num