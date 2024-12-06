import json
import logging

from easybd.db import ETLTableInfo


class TemplateReaderHikapi:
    """
    海康api reader
    """

    def __call__(self, *args):
        if len(args) < 2:
            logging.warning("参数缺失")
            return {}
        table_info: ETLTableInfo = args[0]
        columns = table_info.table_info.table_fields
        source_table = table_info.source_table_info[0].table_info.table_name
        parameter: dict = json.loads(args[1])
        host = parameter.get('host', "host")
        app_key = parameter.get('appKey', "appKey")
        app_secret = parameter.get('appSecret', "appSecret")

        template_reader_hikapi = {
            "name": "hikapireader",
            "parameter": {
                "agreement": "https",
                "host": f"{host}",
                "appKey": f"{app_key}",
                "appSecret": f"{app_secret}",
                "artemisPath": "/artemis",
                "url": f"{source_table}",
                "method": "post",
                "headers": {
                },
                "jsonData": {
                    "pageNo": 1,
                    "pageSize": 1000
                },
                "page": {
                    "ifPage": True,
                    "countField": "data.total",
                    "dataPath": "data.list",
                    "paramPageIndexField": "pageNo",
                    "paramPageSizeField": "pageSize"
                },
                "columns": columns
            }
        }
        return template_reader_hikapi
