from enum import Enum

from easybd.datax.datax_template_writer import *
from easybd.datax.template.reader.template_reader_hdfs import TemplateReaderHdfs
from easybd.datax.template.reader.template_reader_hikapi import TemplateReaderHikapi
from easybd.datax.template.reader.template_reader_mysql import TemplateReaderMysql
from easybd.datax.template.reader.template_reader_postgresql import TemplateReaderPostgresql
from easybd.datax.template.reader.template_reader_stream import TemplateReaderStream
from easybd.datax.template.writer.template_writer_hdfs import TempalteWriterHdfs
from easybd.datax.template.writer.template_writer_mysql import TemplateWriterMysql
from easybd.datax.template.writer.template_writer_pgsql import TemplateWriterPostgresql


class DataXReaderType(Enum):
    STREAM = TemplateReaderStream()
    HIKAPI = TemplateReaderHikapi()
    HDFS = TemplateReaderHdfs()
    PGSQL = TemplateReaderPostgresql()
    MYSQL = TemplateReaderMysql()


class DataXWriterType(Enum):
    STREAM = TemplateWriterStream()
    HIVE = TempalteWriterHive()
    PGSQL = TemplateWriterPostgresql()
    MYSQL = TemplateWriterMysql()
    HDFS = TempalteWriterHdfs()
