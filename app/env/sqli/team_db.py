import pymysql
import random

from utils.dummy import rand
from utils.flag import random_flag
from utils.mysql import sqli_db
from utils.mysql import raw_query

from flag.models import Flag
from env.environ import ITEM_CATEGORY_SQLI
from env.credential import MYSQL_HOST, MYSQL_PORT, MYSQL_ROOT_USER, MYSQL_ROOT_PASS, MYSQL_PASS

SQLI_INIT_SCORE = 500

NUM_TEAM = 5
NUM_TABLE_FLAG = 1
NUM_COLUMN_FLAG = 3
NUM_ELEMENT_FLAG = 10
NUM_FLAG = NUM_TABLE_FLAG + NUM_ELEMENT_FLAG + NUM_COLUMN_FLAG

NUM_TABLE = 10
NUM_COLUMN = 5
NUM_ROW = 100

TABLE_SHOW_INTERVAL = 10

FLAG_MAX_LEN = 50


class Element:
    def __init__(self):
        self.name: str = rand()
        self.size: int = 1
        self.child: list = []

    def insert_flag(self, flag: str):
        count = 0
        while True:
            count += 1
            randIdx = random.randint(0,len(self.child)-1)
            if "PLUS{" not in self.child[randIdx].name:
                self.child[randIdx].name = flag
                return True

            if count == self.size:
                return False


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
                name = rand()
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
        result = "CREATE TABLE " + db_name + ".`" + self.name + "` (" + " VARCHAR(200), ".join("`"+c.name+"`" for c in self.columns) + " VARCHAR(200)); \n"
        cols = "`, `".join(c.name for c in self.columns)

        for e_idx in range(NUM_ROW):
            data = "', '".join(c.elements[e_idx].name for c in self.columns)
            result += f"INSERT INTO {db_name}.`{self.name}` (`{cols}`) VALUES ('{data}'); \n"

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
    Flag.objects.create(flag=flag, score=SQLI_INIT_SCORE, category=ITEM_CATEGORY_SQLI)
    return flag


def get_flag_set(max_len):
    return [add_flag(FLAG_MAX_LEN) for _ in range(NUM_FLAG)]


def generate_db(conn: pymysql.connections.Connection, team_name: str):
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

    raw_query(sqli_db(), f"CREATE DATABASE {team_name};\n"
                        + f"CREATE USER {team_name}@'%' IDENTIFIED BY '{MYSQL_PASS}';\n"
                        + f"GRANT SELECT ON {team_name}.* TO {team_name}@'%';\n"
                        + f"FLUSH privileges;")
    raw_query(sqli_db(team_name, MYSQL_PASS), db.to_sql())
