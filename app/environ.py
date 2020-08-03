from dataclasses import dataclass
from credential import SQLI_CREDENTIAL_USER, SQLI_CREDENTIAL_PASSWD
from credential import FILTER_CREDENTIAL_USER, FILTER_CREDENTIAL_PASSWD

@dataclass
class MySQLConnectionInfo:
    "Connection information to MySQL"
    HOST: str
    PORT: int
    USER: str
    PASSWD: str
    DB: str
    CHARSET: str


SQLI_DB = MySQLConnectionInfo("", 0000, SQLI_CREDENTIAL_USER, SQLI_CREDENTIAL_PASSWD, "sqli", "utf8")
FILTER_DB = MySQLConnectionInfo("", 0000, FILTER_CREDENTIAL_USER, FILTER_CREDENTIAL_PASSWD, "filter", "utf8")
