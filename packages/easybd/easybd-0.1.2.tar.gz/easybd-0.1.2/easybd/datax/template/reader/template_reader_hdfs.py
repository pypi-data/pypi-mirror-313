import json
import logging

from easybd.db import ETLTableInfo
from easybd.datax.template import hive2datax


class TemplateReaderHdfs:
    """
    海康api reader
    """
    def __call__(self, *args):
        if len(args) < 2:
            logging.warning("参数缺失")
            return {}
        table: ETLTableInfo = args[0]
        table_info = table.table_info
        tn = table_info.table_name
        columns = [{"index": index, "type": hive2datax(ft)} for index, ft in enumerate(table_info.table_fields_type)]
        template_reader_hdfs = {
          "name": "hdfsreader",
          "parameter": {
            "defaultFS": "hdfs://server198.bd.jz:9000",
            "fileType": "text",
            "nullFormat": "\\N",
            "path": f"/user/hive/warehouse/jz2.db/{tn}/dt={{bizdate}}/*",
            "column": columns,
            "encoding": "UTF-8",
            "fieldDelimiter": "\u0001"
          }
        }
        return template_reader_hdfs