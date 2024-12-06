import logging

import pandas as pd
from pandas import DataFrame
from typing import List

from easybd.datax import DataXJob, DataXReaderType
from easybd.datax.datax_type import DataXWriterType
from easybd.db import TableInfo, SourceTableInfo, ETLTableInfo
from easybd.db.ddl import DDLType
from easybd.excel.code_type import CodeType


class Excel:
    def __init__(self, file_path, sheet_name="Sheet1"):
        self.file_path = file_path
        self.sheet_name = sheet_name

        self.data: DataFrame = self._get_data()
        self.table_meta: List[ETLTableInfo] = []
        self.table_fields = []  # 表字段
        self.table_fields_source = []  # 表来源字段
        self._create_database_table()

    def get_table(self, table_name):
        """
        获取指定表名的信息
        :param table_name:
        :return:
        """
        for table in self.table_meta:
            if table is not None:
                if table.table_info.table_name == table_name:
                    return table

    def to_datax(self, reader_type: DataXReaderType, writer_type: DataXWriterType, *args):
        datax = DataXJob(reader_type, writer_type, *args)
        return datax.template

    def to_ddl(self, db_type: DDLType, *args):
        return db_type.value(*args)

    def to_dml(self, table: ETLTableInfo, include_null=False):
        target_table_name = table.table_info.table_name
        table_fields = table.source_fields  # 最终查询字段
        if not include_null:
            table_fields = table.source_fields_not_null
            print(table_fields)
        f_str = "\r\n\t,".join(table_fields)
        source_sqls = []
        join_sqls = []
        for source_table in table.source_table_info:
            source_table_alias = source_table.table_alias
            source_table_info = source_table.table_info
            target_fs = source_table.target_fields

            stn = source_table_info.table_name
            source_table_comment = source_table_info.table_comment
            stfs = source_table_info.table_fields
            stfcs = source_table_info.table_fields_comment
            jc = source_table_info.join_clause  # join clause
            if len(jc) > 0:
                print(jc)
                js = f"left join {source_table_alias} on {jc[0]}"
                join_sqls.append(js)
            qfs = []
            target_fn = len(target_fs)
            for index, stf in enumerate(stfs):
                stf = stf if stf != "" else "null"
                # join 字段 没有映射target field
                if index < target_fn:
                    qf = f"{stf} AS {target_fs[index]} -- {stfcs[index]}"
                else:
                    qf = f"{stf} -- {stfcs[index]}"
                if not include_null:
                    if stf == "null":
                        continue
                    else:
                        qfs.append(qf)
                else:
                    qfs.append(qf)
            qfs_str = "\r\n\t,".join(qfs)

            wheres = source_table_info.where
            w_str = ""
            if len(wheres) > 0:
                w_str = "WHERE " + "\r\n\t\tAND\r\n\t\t".join(wheres)

            source_sql = f"""
{source_table_alias} AS (
-- {source_table_comment}
SELECT 
    {qfs_str}
FROM
    jz2.{stn}    
    {w_str}
)      
            """
            source_sqls.append(source_sql)
        join_clauses = "\r\n".join(join_sqls)
        dml_sql = ",\n\t".join(source_sqls)
        final_sql = f"""
WITH
{dml_sql}

-- insert overwrite jz2.{target_table_name} partition(dt='${{bizdate}}')
SELECT 
    {f_str}
FROM 
    t 
{join_clauses}                  
            """
        print(final_sql)
        return final_sql

    def to_java_dto(self, table:ETLTableInfo):
        table_info = table.table_info
        table_fields = table_info.table_fields
        table_fields_comment = table_info.table_fields_comment
        info = zip(table_fields, table_fields_comment)
        fields = [f"//{field_comment}\nprivate String {str(field_name).lower()};" for (field_name, field_comment) in info]
        print("\n" + "\n".join(fields))


    def to_spark_sql(self, table:ETLTableInfo):
        table_info = table.table_info
        table_fields = table_info.table_fields
        table_fields_comment = table_info.table_fields_comment
        info = zip(table_fields, table_fields_comment)
        fields = [f"\"{str(field_name).lower()} -- {field_comment} \" " for (field_name, field_comment) in
                  info]
        print("\n" + "\n,".join(fields))

    def to_json_array(self, table:ETLTableInfo):
        table_info = table.table_info
        table_fields = table_info.table_fields
        fields = [f"\"{str(field_name).lower()}\"" for field_name in
                  table_fields]
        print("\n" + ",\n".join(fields))

    def _get_data(self):
        return pd.read_excel(self.file_path, sheet_name=self.sheet_name, keep_default_na=False)

    def _check_statement(self, row, statement):
        """
        检查是否包含子句
        :param row:
        :param statement:
        :return:
        """
        if statement in row and pd.notna(row[statement]) and row[statement] != "":
            return True
        else:
            return False

    def _parse_source_table(self, df: DataFrame, suf="") -> SourceTableInfo:
        """
        解析来源表
        :param df:
        :param suf:
        :return:
        """
        source_table_name = df.name[0]
        source_table_comment = df.name[1]
        source_table_alias = df.name[2]
        target_fs = df["字段名称"].tolist()
        source_table_fields = df[f"来源字段{suf}"].tolist()
        source_table_fields_comment = df[f"来源字段备注{suf}"].tolist()
        source_table_fields_type = df[f"来源字段类型{suf}"].tolist()
        stw = [w for w in df[f"where{suf}"].tolist() if w not in ("", None)]
        lj_clause = df[df[f"left join{suf}"] != ""][f"left join{suf}"].tolist()
        for item in lj_clause:
            for join_field in item.split("="):
                join_field = join_field.strip()
                if join_field.startswith(source_table_alias):
                    source_table_fields.append(join_field.split(".")[1])
                    source_table_fields_comment.append("")

        t = TableInfo(source_table_name, source_table_comment, source_table_fields, source_table_fields_comment,
                      source_table_fields_type, stw, join_clause=lj_clause)
        st = SourceTableInfo(t, source_table_alias, target_fs)
        return st

    def _parse2table(self, df: DataFrame):
        table_name = df.name[0]
        table_comment = df.name[1]
        table_fields = df["字段名称"].tolist()
        table_fields_comment = df["字段备注"].tolist()
        table_fields_type = df["字段类型"].tolist()
        source_fields = df[["字段备注", "来源表别名", "字段名称"]].apply(lambda x: f"{x[1]}.{x[2]} -- {x[0]}",
                                                                         axis=1).tolist()
        df_not_null = df[df["来源字段"] != '']
        try:
            source_fields_not_null = df_not_null[["字段备注", "来源表别名", "字段名称"]].apply(
                lambda x: f"{x[1]}.{x[2]} -- {x[0]}", axis=1).tolist()
            source_table_info = df.groupby(["来源表", "来源表备注", "来源表别名"]).apply(
                lambda data: self._parse_source_table(data)).tolist()
            # 新增union 表
            if "来源表2" in df.columns and not (df['来源表2'] == '').all():
                source_table_info2 = df.groupby(["来源表2", "来源表备注2", "来源表别名2"]).apply(
                    lambda data: self._parse_source_table(data, "2")).tolist()
                source_table_info = source_table_info + source_table_info2
            t = TableInfo(table_name, table_comment, table_fields, table_fields_comment, table_fields_type)
            etl_t = ETLTableInfo(t, source_table_info, source_fields, source_fields_not_null=source_fields_not_null)
            return etl_t
        except AttributeError as e:
            logging.error(f"{table_name}  表未配置完成")

    def _create_database_table(self):
        t_all = self.data.groupby(["表名", "表备注"]).apply(lambda data: self._parse2table(data)).tolist()
        self.table_meta = t_all

    # def write2zeppelin(self, host: str, port: str, note_dir: str, table_name: str, *code_types):
    #     table = self.get_table(table_name)
    #     paragraphs = []
    #     for code_type in code_types:
    #         if code_type == CodeType.DDL_HIVE:
    #             r = self.to_ddl(DDLType.HIVE, table.table_info)
    #             p = Paragraph("ddl_hive", f"%spark\n{r}")
    #             paragraphs.append(p)
    #     note_path = f'{note_dir}/{table_name}'
    #     note = Note(note_path, paragraphs)
    #     zc = ZeppelinClient(host, port)
    #     if not zc.create_note(note):
    #         zc.create_paragraph_list(note_path, paragraphs)
