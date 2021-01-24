from django.contrib.auth import get_user_model
from env.sqli_flags import SQLI_FLAGS



def flag_match_list(flag_input: str):
    return [i for i in SQLI_FLAGS if i[0] is flag_input]


def score(flag_input: str) -> int:
    result = flag_match_list(flag_input)

    if len(result) == 0:
        return 0
    else:
        return result[0][1]