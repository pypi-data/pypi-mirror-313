from easybd.db.table_info import TableInfo
import re


class DDLPgSql:
    def __call__(self, table: TableInfo):
        table_name = table.table_name
        table_name_comment = table.table_comment
        table_fields = table.table_fields
        table_fields_comment = table.table_fields_comment
        table_fields_type = table.table_fields_type
        fields = []
        fields_comment = []

        for i in range(0, len(table_fields)):
            # column_name = camel_to_snake(table_fields[i])
            column_name = table_fields[i]
            column_comment = "" if isinstance(table_fields_comment[i], float) else table_fields_comment[i]
            tft_upper = table_fields_type[i].upper()
            if tft_upper == "NUMBER" or tft_upper.startswith("TINYINT") or tft_upper.startswith("INT") or tft_upper.startswith("NUMERIC") or tft_upper.startswith("BIGINT"):
                column_type = "int"
            elif tft_upper == "BOOL":
                column_type = "BOOLEAN"
            elif tft_upper in ("STRING", 'MEDIUMTEXT') or tft_upper.startswith("TIMESTAMPTZ"):
                column_type = "varchar(255)"
            else:
                column_type = "text"
            field = f"{column_name} {column_type}"
            field_comment = f"COMMENT ON COLUMN {table_name}.{column_name} IS '{column_comment}';"
            fields.append(field)
            fields_comment.append(field_comment)
        all_field = ",\r\n\t".join(fields)
        all_field_comment = "\r\n".join(fields_comment)
        sqls = f"""
-- {table_name}
CREATE TABLE public.{table_name}
(
    {all_field}
)
;
COMMENT ON TABLE {table_name} IS '{table_name_comment}';
{all_field_comment}

                """
        return sqls
