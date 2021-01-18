from django.apps import AppConfig
from django.contrib.auth import get_user_model

import pymysql
import random

from utils.generator import random_string, random_flag
from utils.mysql import sqli_db
from utils.mysql import raw_query

from flag.models import Flag
from env.environ import ITEM_CATEGORY_SQLI, SQLI_SCORE
import base.models
from .models import SqliLog
from env.credential import MYSQL_PASS


Team = get_user_model()


class SqliConfig(AppConfig):
    name = 'sqli'



NUM_TEAM = 6
NUM_TABLE_FLAG = 1
NUM_COLUMN_FLAG = 2
NUM_ELEMENT_FLAG = 7
NUM_FLAG = NUM_TABLE_FLAG + NUM_ELEMENT_FLAG + NUM_COLUMN_FLAG

NUM_TABLE = 10
NUM_COLUMN = 5
NUM_ROW = 100

TABLE_SHOW_INTERVAL = 10

FLAG_MAX_LEN = 50


class Element:
    def __init__(self):
        self.name: str = random_string()
        self.size: int = 1
        self.child: list = []

    def insert_flag(self, flag: str):
        count = 0
        candidates = [i for i,value in enumerate(self.child) if not str(value).startswith("PLUS{")]
        if not candidates:
            return False 
        self.child[random.choice(candidates)].name = flag
        return True


class Column(Element):
    def __init__(self):
        super().__init__()
        self.elements: list = [Element() for _ in range(NUM_ROW)]
        self.child = self.elements
        self.size: int = NUM_ROW

    def __repr__(self):
        return self.name

    def __str__(self):
        return self.name


class Table(Element):
    def __init__(self):
        super().__init__()
        self.columns: list = [Column() for _ in range(NUM_COLUMN)]
        self.child = self.columns
        self.size: int = NUM_COLUMN

        names = []

        for c in self.columns:
            while True:
                name = random_string()
                if name not in names:
                    c.name = name
                    names.append(name)
                    break

    def __repr__(self):
        return self.name

    def __str__(self):
        return self.name

    def show(self):
        print(self.name)
        print("-" * (NUM_COLUMN * 13))
        for i in self.columns:
            print("%10s |" % (i.name[:10]), end=' ')
        print()
        print("-" * (NUM_COLUMN * 13))
        for e_idx in range(NUM_ROW):
            for col in self.columns:
                print("{:10s} |".format(col.elements[e_idx].name[:10]), end=' ')
            print()
        print("-" * (NUM_COLUMN * 13))
        print()

    def to_sql(self, db_name: str):
        result = "CREATE TABLE " + db_name + ".`" + self.name + "` (" + " VARCHAR(100), ".join("`"+c.name+"`" for c in self.columns) + " VARCHAR(100)); \n"
        cols = "`, `".join(c.name for c in self.columns)

        for e_idx in range(NUM_ROW):
            data = "', '".join(c.elements[e_idx].name for c in self.columns)
            result += f"INSERT INTO {db_name}.`{self.name}` (`{cols}`) VALUES ('{data}'); \n"
        print(result)
        return result


class DB(Element):
    def __init__(self, _name: str):
        super().__init__()
        self.name: str = _name
        self.size: int = NUM_TABLE
        self.tables: list = [Table() for _ in range(NUM_TABLE)]
        self.child = self.tables

    def __repr__(self):
        return self.name

    def __str__(self):
        return self.name

    def show(self):
        print(f"[+] DB: {self.name}")
        for t in self.tables:
            t.show()

    def to_sql(self):
        result = ""
        for table in self.tables:
            result += table.to_sql(self.name)
        return result
        


def add_flag(max_len):
    flag = random_flag(max_len)
    Flag.objects.create(flag=flag, score=SQLI_SCORE, category=ITEM_CATEGORY_SQLI)
    return flag


def get_flag_set(max_len):
    return [add_flag(FLAG_MAX_LEN) for _ in range(NUM_FLAG)]


def generate_db(team_name: str):
    idx = 0
    db = DB(team_name)
    team_flag_set = get_flag_set(60)

    for _ in range(NUM_TABLE_FLAG):
        db.insert_flag(team_flag_set[idx])
        idx += 1

    for _ in range(NUM_COLUMN_FLAG):
        table = random.choice(db.tables)
        table.insert_flag(team_flag_set[idx])
        idx += 1

    for _ in range(NUM_ELEMENT_FLAG):
        table = random.choice(db.tables)
        col = random.choice(table.columns)
        col.insert_flag(team_flag_set[idx])
        idx += 1


    query = f"DROP DATABASE IF EXISTS {team_name};\n"
    query += f"CREATE DATABASE {team_name};\n"
    query += f"CREATE USER {team_name}@'%' IDENTIFIED BY '{MYSQL_PASS}';\n"
    query += f"GRANT SELECT ON {team_name}.* TO {team_name}@'%';\n"
    query += f"FLUSH privileges;"

    raw_query(sqli_db(), query)
    raw_query(sqli_db(), db.to_sql())



def query_sql(attack_team_name: str, target_team_name: str, query: str):
    if attack_team_name == target_team_name:
        return False, "Attacked yourself", 400
    
    try:
        target_team = Team.objects.get(username=target_team_name)
    except Team.DoesNotExist:
        return False, "No Such Team", 404

    ok, message, status_code = is_valid_query(target_team, query)
    if not ok:
        return False, message, status_code

    succeed, res = raw_query(sqli_db(target_team_name, MYSQL_PASS), query)

    sqli_log = SqliLog.objects.create()
    sqli_log.from_team = attack_team_name
    sqli_log.to_team = target_team_name
    sqli_log.query = query
    sqli_log.succeed = succeed
    sqli_log.return_value = res
    sqli_log.save()

    return succeed, res, 200



def is_valid_query(target_team: Team, query: str):
    try:
        sqlifilter = base.models.SqliFilter.objects.get(owner=target_team)
    except Team.DoesNotExist:
        return False, "No Such Team", 404

    max_len = sqlifilter.max_len
    if max_len < len(query):
        return False, "Too Long Query", 400

    regex_filter_list = sqlifilter.regex_rule_list.all()
    for r in regex_filter_list:
        p = re.compile(r.regexp, re.I)
        if p.match(query):
            return False, "Blocked by Regex", 400

    return True, "", 200
