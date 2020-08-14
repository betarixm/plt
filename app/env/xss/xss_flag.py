from flag.models import Flag
from env.environ import ITEM_CATEGORY_XSS

def get_flag():
    return Flag.objects.filter(category=ITEM_CATEGORY_XSS, is_added=False)[0]