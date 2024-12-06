from easybd.db import ETLTableInfo


class TemplateWriterStream:
    def __call__(self, *args):
        template = {
            "name": "streamwriter",
            "parameter": {
                "encoding": "UTF-8",
                "print": True
            }
        }
        return template

class TempalteWriterHive:
    def __call__(self, *args):
        if len(args) == 0:
            return {}
        table: ETLTableInfo = args[0]
        table_name = table.table_info.table_name
        columns = [{"name": field, "type": "string"} for field in table.table_info.table_fields]
        template_writer_hive = {
            "name": "hivewriter",
            "parameter": {
                "defaultFS": "hdfs://server198.bd.jz:9000",
                "fileType": "text",
                "jdbcUrl": "jdbc:hive2://server198.bd.jz:10000/jz2",
                "tableName": table_name,
                "path": f"/user/hive/warehouse/jz2.db/{table_name}/dt={{bizdate}}",
                "fileName": "xxxx",
                "column": columns,
                "writeMode": "truncate",
                "fieldDelimiter": "\u0001"
            }
        }
        return template_writer_hive
