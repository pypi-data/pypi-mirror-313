from easybd.db.table_info import TableInfo
import re


class DDLHive:
    def __call__(self, table: TableInfo):
        table_name = table.table_name
        table_name_comment = table.table_comment
        table_fields = table.table_fields
        table_fields_comment = table.table_fields_comment
        table_fields_type = table.table_fields_type
        fields = []

        for i in range(0, len(table_fields)):
            # column_name = camel_to_snake(table_fields[i])
            column_name = table_fields[i]
            column_comment = "" if isinstance(table_fields_comment[i], float) else table_fields_comment[i]
            tft_upper = table_fields_type[i].upper()
            if tft_upper == "NUMBER" or tft_upper.startswith("TINYINT") or tft_upper.startswith("INT") or tft_upper.startswith("NUMERIC") or tft_upper.startswith("BIGINT"):
                column_type = "INT"
            elif tft_upper == "BOOL":
                column_type = "BOOLEAN"
            elif tft_upper in ("STRING", "TEXT", 'MEDIUMTEXT') or tft_upper.startswith("TIMESTAMPTZ"):
                column_type = "STRING"
            elif tft_upper.startswith("DATE"):
                column_type = "STRING"
            else:
                column_type = re.sub(r'varchar\(\d*\)', 'STRING', table_fields_type[i])
            column_type = re.sub(r"\d+", "", column_type) # 替换所有数字
            field = f"{column_name} {column_type} COMMENT '{column_comment}'"
            fields.append(field)
        all_field = ",\r\n\t".join(fields)
        sqls = f"""
-- {table_name}
-- DROP TABLE IF EXISTS jz2.{table_name};
CREATE TABLE IF NOT EXISTS jz2.{table_name}
(
    {all_field}
)
comment '{table_name_comment}'
partitioned by (dt string)
ROW FORMAT DELIMITED
FIELDS TERMINATED BY '\\001'
;
                """
        return sqls
