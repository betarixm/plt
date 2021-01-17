import pymysql
from pymysql.constants import CLIENT
from env.credential import MYSQL_HOST, MYSQL_PORT, MYSQL_ROOT_USER, MYSQL_ROOT_PASS


def sqli_db(user=MYSQL_ROOT_USER, password=MYSQL_ROOT_PASS) -> pymysql.connections.Connection:
    """
    Make Connection to sqli mysql server
    :return: sqli; pymysql Connection Object
    """
    return pymysql.connect(host=MYSQL_HOST, 
                            port=MYSQL_PORT, 
                            user=user, 
                            password=password, 
                            charset="utf8", 
                            client_flag=CLIENT.MULTI_STATEMENTS,)


def raw_query(conn: pymysql.connections.Connection, query: str):
    """
    Query Dangerously & Close DB Connection.
    :param conn: pymysql Connection Object
    :param query: Query Sentence
    :return: is_success, result
    """
    try:
        c = conn.cursor()
        c.execute(query)
        return True, c.fetchall()
    except Exception as e:
        print("ERROROROROROROR!!!!!:",e)
        return False, e
    finally:
        conn.close()