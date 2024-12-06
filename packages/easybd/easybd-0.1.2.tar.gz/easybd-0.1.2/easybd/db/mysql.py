from easybd.db.core import BaseDB
from urllib.parse import quote_plus as urlquote
from sqlalchemy import text


class Mysql(BaseDB):
    """"""

    def __init__(self, host, port, username, password, dbname, table_names: list = None):
        """
        # default
        engine = create_engine("mysql://scott:tiger@localhost/foo")

        # mysqlclient (a maintained fork of MySQL-Python)
        engine = create_engine("mysql+mysqldb://scott:tiger@localhost/foo")

        # PyMySQL
        engine = create_engine("mysql+pymysql://scott:tiger@localhost/foo")

        :param host: ip
        :param port: 端口
        :param username: 用户名
        :param password: 密码
        :param dbname: 数据库
        """

        url = f"mysql+pymysql://{username}:{urlquote(password)}@{host}:{port}/{dbname}"

        where = f"TABLE_SCHEMA = '{dbname}'"
        if table_names:
            tables = str(table_names).replace("[","(").replace("]",")")
            where = where + f" and TABLE_NAME in {tables}"

        sql_table_comment = f"""
                SELECT TABLE_NAME, TABLE_COMMENT, TABLE_ROWS
                FROM information_schema.TABLES 
                WHERE {where}
                """
        sql_table_column = f"""
                SELECT 
                    TABLE_NAME,
                    COLUMN_NAME,
                    COLUMN_TYPE,
                    COLUMN_COMMENT
                FROM 
                    INFORMATION_SCHEMA.COLUMNS
                WHERE 
                    TABLE_SCHEMA = '{dbname}';
        """

        super().__init__(url, sql_table_comment, sql_table_column)



