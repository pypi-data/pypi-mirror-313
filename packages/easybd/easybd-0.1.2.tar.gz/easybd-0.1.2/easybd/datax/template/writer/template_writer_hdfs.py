from easybd.db import ETLTableInfo


class TempalteWriterHdfs:
    def __call__(self, *args):
        if len(args) == 0:
            return {}
        table: ETLTableInfo = args[0]
        table_name = table.table_info.table_name
        columns = [{"name": field, "type": "string"} for field in table.table_info.table_fields]
        template_writer_hdfs = {
            "name": "hdfswriter",
            "parameter": {
                "defaultFS": "hdfs://server198.bd.jz:9000",
                "fileType": "text",
                "path": f"/user/hive/warehouse/jz2.db/{table_name}/dt={{bizdate}}",
                "fileName": "xxxx",
                "column": columns,
                "writeMode": "truncate",
                "fieldDelimiter": "\u0001"
            }
        }
        return template_writer_hdfs