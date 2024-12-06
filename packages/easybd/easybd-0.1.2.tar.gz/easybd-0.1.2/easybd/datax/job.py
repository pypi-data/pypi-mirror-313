import json

from easybd.datax.datax_type import DataXReaderType, DataXWriterType


class DataXJob:
    """
    用于构建datax job
    """

    def __init__(self, reader_type: DataXReaderType, writer_type: DataXWriterType, *args):
        self.reader_type = reader_type
        self.writer_type = writer_type
        self.args = args
        self._template = {
            "job": {
                "setting": {
                    "speed": {
                        "channel": 2
                    },
                    "errorLimit": {
                        "record": 0,
                        "percentage": 0.02
                    }
                },
                "content": [
                    {
                        "reader": {},
                        "writer": {}
                    }
                ]
            }
        }
        self._build()
        self.template = json.dumps(self._template, indent=4, ensure_ascii=False)

    def _build(self):
        self._build_reader()
        self._build_writer()

    def _build_reader(self):
        self._template['job']['content'][0]['reader'] = self.reader_type.value(*self.args)

    def _build_writer(self):
        self._template['job']['content'][0]['writer'] = self.writer_type.value(*self.args)
