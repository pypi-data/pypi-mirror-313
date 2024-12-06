
class TemplateReaderStream:
    def __call__(self, *args):
        template = {
            "name": "streamreader",
            "parameter": {
                "sliceRecordCount": 10,
                "column": [
                    {
                        "type": "long",
                        "value": "10"
                    },
                    {
                        "type": "string",
                        "value": "hello，你好，世界-DataX"

                    }
                ]
            }
        }
        return template
