from easybd.conf import JDBCConf
from easybd.db import ETLTableInfo


class TemplateWriterMysql:
    def __call__(self, *args):
        if len(args) == 0:
            return {}
        table: ETLTableInfo = args[0]
        jdbc_conf: JDBCConf = args[1]

        table_name = table.table_info.table_name
        columns = [f"`{field}`" for field in table.table_info.table_fields]
        template_writer_mysql = {
            "name": "mysqlwriter",
            "parameter": {
                "username": jdbc_conf.user,
                "password": jdbc_conf.passwd,
                "column": columns,
                "preSql": [
                    f"truncate table {table_name}"
                ],
                "connection": [
                    {
                        "jdbcUrl": jdbc_conf.jdbc_url,
                        "table": [
                            table_name
                        ]
                    }
                ],
                "postSql": []
            }
        }
        return template_writer_mysql
