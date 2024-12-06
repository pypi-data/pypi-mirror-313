from easybd.db.ddl import DDLType
from easybd.excel import Excel


e = Excel("D:\wjn\yx\schooletl\doc\sr\etl_schema.xlsx")
table = e.get_table("ods_sr_hz_hik_clbk")

def test_ddl2pg():
    r = e.to_ddl(DDLType.PgSql, table.table_info)
    print(r)

def test_to_json_array():
    e.to_json_array(table)