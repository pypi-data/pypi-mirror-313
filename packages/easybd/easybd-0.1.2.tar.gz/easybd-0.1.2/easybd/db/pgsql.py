from easybd.db.core import BaseDB
from urllib.parse import quote_plus as urlquote


class PostgreSql(BaseDB):
    def __init__(self, host, port, username, password, dbname, schema, table_names: list = None):
        """
        # default
        engine = create_engine("postgresql://scott:tiger@localhost/mydatabase")

        # psycopg2
        engine = create_engine("postgresql+psycopg2://scott:tiger@localhost/mydatabase")

        # pg8000
        engine = create_engine("postgresql+pg8000://scott:tiger@localhost/mydatabase")


        """
        if table_names:
            tables = str(table_names).replace("[","(").replace("]",")")
            filter_table = f"and tablename in {tables}"
        else:
            filter_table = ""

        sql_table_comment = f"""
                        select
                            relname as "TABLE_NAME",
                            cast (
                                obj_description (relfilenode, 'pg_class') as varchar
                            ) as "TABLE_COMMENT",
                            reltuples as "TABLE_ROWS"
                        from
                            pg_class c
                        where
                            relname in (
                                select
                                    tablename
                                from
                                    pg_tables
                                where
                                    schemaname = '{schema}'
                                    {filter_table}
                            )
                            and relnamespace in (select oid from pg_namespace where nspname = '{schema}')
                            ;
                        """
        sql_table_col = f"""
                        select
                          a.attnum as "序号",
                          c.relname as "TABLE_NAME",
                          cast(obj_description(c.oid) as varchar) as "TABLE_COMMENT",
                          a.attname as "COLUMN_NAME",
                          concat_ws('', t.typname, SUBSTRING(format_type(a.atttypid, a.atttypmod) from '\(.*\)')) as "COLUMN_TYPE",
                          d.description as "COLUMN_COMMENT"
                        from
                          (
                            select 
                              * 
                            from 
                              pg_attribute 
                            where 
                              attisdropped = 'f' -- 过滤打删除标识的列
                          ) a
                        left join pg_description d on
                          d.objoid = a.attrelid
                          and d.objsubid = a.attnum
                        left join (select * from pg_class where relnamespace in (select oid from pg_namespace where nspname = '{schema}') ) c on
                          a.attrelid = c.oid
                        left join pg_type t on
                          a.atttypid = t.oid
                        where
                          a.attnum >= 0
                          and c.relname in (
                            select
                                tablename
                            from
                                pg_tables
                            where
                                schemaname = 'public'
                          )
                        order by
                          c.relname desc,
                          a.attnum asc

            """
        url = f"postgresql+psycopg2://{username}:{urlquote(password)}@{host}:{port}/{dbname}"
        super().__init__(url, sql_table_comment, sql_table_col)


if __name__ == '__main__':
    pg = PostgreSql("192.168.3.215", "5432", "postgres", "Pgsql@2024", "postgres", "public",
                         table_names=['t_info_long_staff_account'])
    pg.table_info_to_excel("jz2.xlsx")