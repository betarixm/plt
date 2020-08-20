from flag.models import Flag
from env.environ import ITEM_CATEGORY_XSS
from utils.flag import random_flag

XSS_INIT_SCORE = 200

def get_flag():
    flag = random_flag()
    Flag.objects.create(flag=flag, score=XSS_INIT_SCORE, category=ITEM_CATEGORY_XSS)
    return flag