import random
import string


def random_int(length=5):
    return str(random.randint(10**length, 10**(length+1)-1))


def random_string(length=10):
    return ''.join(random.choice(string.ascii_letters) for i in range(length))


def random_flag(max_len=100):
    length = (max_len - 9) // 4
    return 'PLUS{'+random_int(length)+'.'+random_int(length)+'-'+random_int(length)+'.'+random_int(length)+'}'
