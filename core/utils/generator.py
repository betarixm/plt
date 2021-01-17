import random
import string

def random_string(length=10):
    return ''.join(random.choice(string.ascii_letters) for i in range(length))

def random_flag(max_len=100):
    return 'PLUS{'+random_string(max_len-6)+'}'