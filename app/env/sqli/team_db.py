import pymysql
from utils.dummy import rand
from utils.flag import random_flag
import random
from flag.models import Flag
from env.environ import ITEM_CATEGORY_SQLI
from env.credential import MYSQL_HOST, MYSQL_PORT, MYSQL_USER, MYSQL_PASS

INIT_SCORE = 500

NUM_TEAM = 5
NUM_TABLE_FLAG = 2
NUM_COLUMN_FLAG = 2
NUM_ELEMENT_FLAG = 6
NUM_FLAG = NUM_TABLE_FLAG + NUM_ELEMENT_FLAG + NUM_COLUMN_FLAG

NUM_TABLE = 10
NUM_COLUMN = 5
NUM_ROW = 100

TABLE_SHOW_INTERVAL = 10


class Element:
    def __init__(self):
        self.name: str = rand()
        self.size: int = 1
        self.child: list = []

    def insert_flag(self, flag: str):
        count = 0
        while True:
            count += 1
            beta = random.choice(self.child)
            if "PLUS{" not in beta.name:
                beta.name = flag
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
        result = f"CREATE TABLE `{db_name}`.`{self.name}` (`{ ('` VARCHAR(200), `'.join(c.name for c in self.columns))}` VARCHAR(200)); \n"
        cols = f"`{'`, `'.join(c.name for c in self.columns)}`"

        for e_idx in range(NUM_ROW):
            data = f"`{'`, `'.join(c.elements[e_idx].name for c in self.columns)}`"
            result += f"INSERT INTO `{db_name}`.`{self.name}` ({cols}) VALUES ({data}); \n"

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
        result = f"CREATE DATABASE `{self.name}`;\n"
        for table in self.tables:
            result += table.to_sql(self.name)
        print(result)
        return result

    def query(self, conn: pymysql.Connection):
        try:
            with conn.cursor() as cursor:
                cursor.execute(self.to_sql())
            conn.commit()
        finally:
            conn.close()


def add_flag():
    while True:
        flag = random_flag()
        if len(Flag.objects.filter(flag=flag)) == 0:
            Flag.objects.create(flag=flag, score=INIT_SCORE, category=ITEM_CATEGORY_SQLI)
            return flag


def get_flag_set():
    return [add_flag() for _ in range(NUM_FLAG)]


def generate_db(conn: pymysql.Connection, team_name: str):
    idx = 0
    db = DB(team_name)
    team_flag_set = get_flag_set()

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

    db.query(conn)

