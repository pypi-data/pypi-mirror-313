import logging
from urllib.parse import quote_plus


class JDBCConf:
    """
    Configuration jdbc info

    """
    def __init__(self, dbtype, host, port, dbname, user, passwd):
        self.dbtype = dbtype
        self.host = host
        self.port = port
        self.dbname = dbname
        self.user = user
        self.passwd = passwd

        if dbtype == "mysql":
            self.jdbc_url = f"jdbc:mysql://{host}:{port}/{dbname}?useSSL=false&characterEncoding=utf8&character_set_server=utf8mb4&rewriteBatchedStatements=true&serverTimezone=Asia/Shanghai&tinyInt1isBit=false"
        elif dbtype == "pgsql":
            self.jdbc_url = f"jdbc:postgresql://{host}:{port}/{dbname}"
        else:
            logging.warning(f"there no config dbtype: {dbtype}")


