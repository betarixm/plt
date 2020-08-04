import pymysql
from env.environ import *


def sqli_db() -> pymysql.connections.Connection:
    """
    Make Connection to sqli mysql server
    :return: sqli; pymysql Connection Object
    """
    return pymysql.connect(host=SQLI_DB.HOST, port=SQLI_DB.PORT, user=SQLI_DB.USER,
                           passwd=SQLI_DB.PASSWD, db=SQLI_DB.DB,
                           charset=SQLI_DB.CHARSET)


def raw_query(db: pymysql.connections.Connection, query: str):
    """
    Query Dangerously & Close DB Connection.
    :param db: pymysql Connection Object
    :param query: Query Sentence
    :return: is_success, result
    """
    try:
        c = db.cursor()
        c.execute(query)
        return True, c.fetchall()
    except Exception as e:
        return False, e
    finally:
        db.close()
