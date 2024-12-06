import logging

from easybd.conf import JDBCConf
from easybd.db import ETLTableInfo


class TemplateReaderMysql:
    def __call__(self, *args):
        if len(args) < 2:
            logging.warning("参数缺失")
            return {}
        table: ETLTableInfo = args[0]
        jdbc_conf: JDBCConf = args[1]
        table_info = table.table_info
        tn = table_info.table_name
        columns = table_info.table_fields
        host = jdbc_conf.host
        port = jdbc_conf.port
        db = jdbc_conf.dbname
        username = jdbc_conf.user
        password = jdbc_conf.passwd

        template = {
            "name": "mysqlreader",
            "parameter": {
                # 数据库连接用户名
                "username": username,
                # 数据库连接密码
                "password": password,
                "column": columns,
                # 切分主键
                # "splitPk": "id",
                "connection": [
                    {
                        "table": [
                            tn
                        ],
                        "jdbcUrl": [
                            f"jdbc:mysql://{host}:{port}/{db}?useSSL=false&characterEncoding=utf8&character_set_server=utf8mb4&rewriteBatchedStatements=true&serverTimezone=Asia/Shanghai"
                        ]
                    }
                ]
            }
        }
        return template
