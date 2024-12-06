from easybd.conf import JDBCConf
from easybd.db import ETLTableInfo


class TemplateWriterPostgresql:
    def __call__(self, *args):
        if len(args) == 0:
            return {}
        table: ETLTableInfo = args[0]
        jdbc_conf: JDBCConf = args[1]

        table_name = table.table_info.table_name
        columns = [field for field in table.table_info.table_fields]
        template_writer_hive = {
            "name": "postgresqlwriter",
            "parameter": {
                "username": jdbc_conf.user,
                "password": jdbc_conf.passwd,
                "column": columns,
                "preSql": [],
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
        return template_writer_hive
