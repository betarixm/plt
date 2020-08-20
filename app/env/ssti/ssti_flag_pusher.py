from flag.models import Flag
from env.environ import ITEM_CATEGORY_SSTI
from utils.flag import random_flag

SSTI_INIT_SCORE = 100

def get_flag():
    flag = random_flag()
    Flag.objects.create(flag=flag, score=SSTI_INIT_SCORE, category=ITEM_CATEGORY_SSTI)
    return flag


def deploy_flag():
    with open("flag.txt","w") as f:
        f.write(get_flag())
