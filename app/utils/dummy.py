import random
import string

def rand():
    return ''.join(random.choice(string.ascii_letters) for i in range(10))
