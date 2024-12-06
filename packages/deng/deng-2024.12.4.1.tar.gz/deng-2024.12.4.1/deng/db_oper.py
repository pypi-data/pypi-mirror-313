#!/usr/bin/env python
# -*- coding: UTF-8 -*-
"""数据库操作
1. db_data_stat: 数据库数据量统计
2. compare_database: 比较两个数据库的表结构，找到差异，以db1为基准，找出db2中缺失的表，以及表结构的差异
@author: deng
@file: db_oper.py
@time: 2024/10/22 下午7:38
"""
import logging
from copy import deepcopy
from typing import Dict, List, Tuple, Union

import pymysql
from pymysql.connections import Connection
from pymysql.cursors import DictCursor
from deng import logger, configure_logger
from deng import my_http as http_utils


configure_logger(level=logging.INFO)


def get_connection(
    host: str,
    port: int,
    username: str,
    password: str,
    database: str = None,
    charset="utf8mb4",
) -> Connection:
    """获取数据库连接"""
    connection = pymysql.connect(
        host=host,
        port=port,
        user=username,
        password=password,
        database=database,
        charset=charset,
        cursorclass=DictCursor,
    )

    return connection


def db_data_stat(
    host: str,
    port: int,
    username: str,
    password: str,
    database: str = None,
    ignore_databases: list = None,
) -> Dict[str, Dict[str, int]]:
    """Database 数据量统计"""
    db_info = dict()
    if ignore_databases is None:
        ignore_databases = [
            "mysql",
            "information_schema",
            "performance_schema",
            "sys",
            "test",
        ]
    connection = get_connection(host, port, username, password, database)

    try:
        with connection.cursor() as cursor:
            # 获取数据库中的Database
            cursor.execute("SHOW DATABASES")
            databases = cursor.fetchall()
            http_utils.format_output(databases, level="debug")

            # 遍历每张表并获取行数
            for _database in databases:
                # 指定了特定数据库时，忽略其余的数据库
                if database and database != _database["Database"]:
                    logger.warning(f"忽略Database: {_database['Database']}")
                    continue

                # 忽略系统数据库
                if _database["Database"] in ignore_databases:
                    logger.warning(f"忽略Database: {_database['Database']}")
                    continue

                # 指定数据库
                cursor.execute(f"USE `{_database['Database']}`")

                # 读取数据库中的表数据
                logger.info(f"开始遍历Database: {_database['Database']}")
                table_info = read_db_by_name(cursor, _database["Database"])
                db_info[_database["Database"]] = table_info
    finally:
        # 关闭数据库连接
        connection.close()

    # 按表名称重新排序
    db_info = dict(sorted(db_info.items()))
    return db_info


def read_db_by_name(cursor: DictCursor, database: str) -> dict:
    """读取数据库中的表数据"""
    table_info = dict()
    # 获取数据库中的所有表
    cursor.execute("SHOW TABLES")
    tables = cursor.fetchall()
    http_utils.format_output(tables, level="debug")

    # 遍历每张表并获取行数
    for table in tables:
        table_name = table[f"Tables_in_{database}"]
        cursor.execute(f"SELECT COUNT(*) as count FROM `{table_name}`")
        result = cursor.fetchone()
        row_count = result["count"]
        table_info[table_name] = row_count
        if row_count > 0:
            logger.info(f"Table: {table_name}, Rows: {row_count}")
        else:
            logger.warning(f"表中没有数据：Table: {table_name}, Rows: {row_count}")
    # 按表名称重新排序
    table_info = dict(sorted(table_info.items()))
    return table_info


def echo_result(db_info: dict):
    """输出结果"""
    # 深度拷贝
    db_info_new = deepcopy(db_info)
    http_utils.format_output(db_info_new, level="info")

    # 提取有数据的表
    for db_name, table_info in db_info_new.items():
        for table_name, row_count in list(table_info.items()):
            if row_count > 0:
                del table_info[table_name]

    http_utils.format_output(db_info_new, level="info")


def get_databases(cursor: DictCursor) -> set:
    cursor.execute("SHOW DATABASES")
    return set(row["Database"] for row in cursor.fetchall())


def get_tables(cursor: DictCursor, database: str) -> set:
    cursor.execute("SHOW TABLES")
    return set(row[f"Tables_in_{database}"] for row in cursor.fetchall())


def compare_columns(table: str, columns1: Union[List, Tuple], columns2: Union[List, Tuple]):
    """比较两个表的字段，以columns1为基准，比较columns2中缺失的字段，以及字段的差异"""
    column_names1 = [column["Field"] for column in columns1]
    column_names2 = [column["Field"] for column in columns2]

    missing_columns = set(column_names1) - set(column_names2)
    if missing_columns:
        logger.warning(f"Table: {table} 中缺失的字段：{missing_columns}")
    else:
        logger.info(f"Table: {table} 中没有缺失字段")

    for column in columns1:
        column_name = column["Field"]
        column2 = next(
            (c for c in columns2 if c["Field"] == column_name), None
        )
        if column2 is None:
            continue

        if column != column2:
            # 字段定义不一致时，找出不一致的地方
            for key, value in column.items():
                if column2[key] != value:
                    logger.warning(f"表【{table}】中字段【{column_name}】的属性【{key}】不一致，标准库为【{value}】，比较库为【{column2[key]}】")
        else:
            logger.info(f"Table: {table} 字段: {column_name} 的定义一致")


def compare_indexes(table: str, indexes1: Union[List, Tuple], indexes2: Union[List, Tuple]):
    """比较两个表的索引，以indexes1为基准，比较indexes2中缺失的索引，以及索引的差异"""
    index_names1 = [index["Key_name"] for index in indexes1]
    index_names2 = [index["Key_name"] for index in indexes2]

    missing_indexes = set(index_names1) - set(index_names2)
    if missing_indexes:
        logger.warning(f"Table: {table} 中缺失的索引：{missing_indexes}")
    else:
        logger.info(f"Table: {table} 中没有缺失索引")

    # 获取索引交集
    common_indexes = set(index_names1) & set(index_names2)

    # 索引重新排序，第一序列Key_name，第二序列Seq_in_index
    indexes1 = sorted(indexes1, key=lambda x: (x["Key_name"], x["Seq_in_index"]))
    indexes2 = sorted(indexes2, key=lambda x: (x["Key_name"], x["Seq_in_index"]))

    # 去掉索引的基数
    for index in indexes1:
        if "Cardinality" in index:
            index.pop("Cardinality")
    for index in indexes2:
        if "Cardinality" in index:
            index.pop("Cardinality")

    # 将所有索引整合成一个元素，主要是处理复合多列索引
    index1_dict = dict()
    index2_dict = dict()
    for index in common_indexes:
        index1_dict[index] = [i for i in indexes1 if i["Key_name"] == index]
        index2_dict[index] = [i for i in indexes2 if i["Key_name"] == index]

    # 比较索引
    for index_name in common_indexes:
        index1 = index1_dict[index_name]
        index2 = index2_dict[index_name]
        if index1 != index2:
            logger.warning(f"Table: {table} 索引: {index_name} 的定义不一致")
            logger.warning(f"db1: {index1}")
            logger.warning(f"db2: {index2}")
        else:
            logger.info(f"Table: {table} 索引: {index_name} 的定义一致")


def compare_database(
    host1: str,
    port1: int,
    username1: str,
    password1: str,
    host2: str,
    port2: int,
    username2: str,
    password2: str,
    databases: list,
    charset1="utf8mb4",
    charset2="utf8mb4",
):
    """比较两个数据库的表结构，以db1为基准，比较db2中缺失的表，以及表结构的差异
    包括表名、字段名、字段类型、字段长度、字段默认值、字段是否为空、字段是否自增、字段是否主键、字段是否唯一、字段是否索引等一系统功能
    只要有任意一处不同，就输出不同的地方
    """
    connection1 = get_connection(host1, port1, username1, password1, charset=charset1)
    connection2 = get_connection(host2, port2, username2, password2, charset=charset2)

    try:
        with connection1.cursor() as cursor1, connection2.cursor() as cursor2:
            # 获取数据库中的Database
            db1_databases = get_databases(cursor1)
            db2_databases = get_databases(cursor2)
            logger.info(db1_databases)
            logger.info(db2_databases)

            for db in databases:
                # 判断数据库是否存在
                if db not in db1_databases:
                    logger.warning(f"Database: {db} 不存在于基准库【{host1}:{port1}】中，请检查")
                    continue

                if db not in db2_databases:
                    logger.warning(f"Database: {db} 不存在于比较库【{host2}:{port2}】中，跳过后续比较步骤")
                    continue

                cursor1.execute(f"USE `{db}`")
                cursor2.execute(f"USE `{db}`")

                # 比较层级一：database层面，比较database创建语句的差异
                sql_txt = f"SHOW CREATE DATABASE `{db}`"
                cursor1.execute(sql_txt)
                db1_define_sql = cursor1.fetchone()
                cursor2.execute(sql_txt)
                db2_define_sql = cursor2.fetchone()
                if db1_define_sql != db2_define_sql:
                    logger.warning(f"Database: {db} 的创建语句不一致")
                    logger.warning(f"db1: {db1_define_sql}")
                    logger.warning(f"db2: {db2_define_sql}")
                else:
                    logger.info(f"Database: {db} 的创建语句一致：{db1_define_sql}")

                # 比较层级二：table 数量层面，获取db2中缺少的表
                db1_tables = get_tables(cursor1, db)
                db2_tables = get_tables(cursor1, db)
                missing_tables = db1_tables - db2_tables
                if missing_tables:
                    logger.warning(
                        f"URL: {host2}:{port2} Database2: {db} 中缺失的表：{missing_tables}"
                    )
                else:
                    logger.info(f"URL: {host2}:{port2} Database2: {db} 中没有缺失表")

                # 比较层级三：table 定义层面
                common_tables = db1_tables & db2_tables
                for table in common_tables:
                    logger.info(f"比较表: {table}")

                    # 比较字段
                    cursor1.execute(f"SHOW COLUMNS FROM `{table}`")
                    cursor2.execute(f"SHOW COLUMNS FROM `{table}`")
                    columns1 = cursor1.fetchall()
                    columns2 = cursor2.fetchall()
                    compare_columns(table, columns1, columns2)

                    # 比较索引
                    cursor1.execute(f"SHOW INDEX FROM `{table}`")
                    cursor2.execute(f"SHOW INDEX FROM `{table}`")
                    indexes1 = cursor1.fetchall()
                    indexes2 = cursor2.fetchall()
                    compare_indexes(table, indexes1, indexes2)
    finally:
        # 关闭数据库连接
        connection1.close()
        connection2.close()


if __name__ == "__main__":
    pass
