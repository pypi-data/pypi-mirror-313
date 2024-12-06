from dataclasses import dataclass, field
from typing import List


@dataclass
class TableInfo:
    table_name: str
    table_comment: str
    table_fields: List[str]
    table_fields_comment: List[str]
    table_fields_type: List[str]
    where: List[str] = field(default_factory=list)  # 默认值为空列表
    join_clause: List[str] = field(default_factory=list)  # 默认值为空列表


@dataclass
class SourceTableInfo:
    table_info: TableInfo
    table_alias: str
    target_fields: List[str] # 目标字段


@dataclass
class ETLTableInfo:
    table_info: TableInfo
    source_table_info: List[SourceTableInfo]
    source_fields: List[str] # 来源字段 顺序排列
    source_fields_not_null: List[str] # 来源字段 不包含为null的 顺序排列
