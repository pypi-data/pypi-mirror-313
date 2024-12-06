from enum import Enum

from easybd.db.ddl.ddl_hive import DDLHive
from easybd.db.ddl.ddl_pgsql import DDLPgSql


class DDLType(Enum):
    HIVE = DDLHive()
    PgSql = DDLPgSql()