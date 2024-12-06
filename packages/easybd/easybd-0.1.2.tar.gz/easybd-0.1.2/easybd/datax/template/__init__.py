def hive2datax(hive_type:str):
    hive_type_upper = hive_type.upper()
    datax_type = "String"
    if hive_type_upper in ("TINYINT","SMALLINT","INT","BIGINT"):
        datax_type = "Long"
    return datax_type