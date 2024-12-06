#!/usr/bin/env python
# -*- coding: UTF-8 -*-
"""
@Author: MaJian
@Time: 2024/1/20 11:30
@SoftWare: PyCharm
@Project: mortal
@File: __init__.py
"""
__all__ = ["MortalSQL", "MortalExecute"]
from .orm_main import MortalSQLMain
from .execute_main import MortalExecuteMain


class MortalSQL(MortalSQLMain):
    def __init__(self, config):
        self._mortal_config = config
        super().__init__(config)

    def session(self, logging_token=None):
        return self._create_session(logging_token)

    def close_session(self, session):
        return self._close_session(session)

    def get_table(self, table):
        return self._get_table(table)

    def alias(self, table):
        return self._alias(table)

    def column(self, table, column):
        return self._column(table, column)

    def get_create_tables_data(self, schema, table):
        return self._get_create_tables_data(schema, table)

    def create_orm(self, read_tables=None, create_tables=None, key_long=False):
        self._create_orm(read_tables, create_tables, key_long)

    def show_column(self, table_name):
        return self._show_column(table_name)

    def get_columns(self, table_name):
        return self._get_columns(table_name)

    def get_tables(self):
        return self._get_tables()

    def drop(self, table_name):
        self._drop(table_name)

    def drop_all(self):
        return self._drop_all()

    def to_dict(self, result):
        return self._to_dict(result)

    def query(self, sql, args=None, kwargs=None):
        return self._query(sql, args, kwargs)

    def execute(self, sql, args=None, kwargs=None):
        self._execute(sql, args, kwargs)

    def fetchone(self, sql, args=None, kwargs=None):
        return self._fetchone(sql, args, kwargs)

    def fetchmany(self, sql, args=None, kwargs=None, many=1):
        return self._fetchmany(sql, args, kwargs, many)

    def fetchall(self, sql, args=None, kwargs=None):
        return self._fetchall(sql, args, kwargs)

    def read_sql(self, table_sql, coerce_float=False, **kwargs):
        return self._read_sql(table_sql, coerce_float, **kwargs)

    def to_sql(self, data, table_name, if_exists='append'):
        self._to_sql(data, table_name, if_exists)

    def mortal_execute(self):
        return MortalExecute(self._mortal_config)

    def close(self):
        self._close()


class MortalExecute(MortalExecuteMain):
    def __init__(self, config):
        super().__init__(config)

    def execute(self, sql, args=None, kwargs=None):
        self._execute(sql, args, kwargs)

    def commit(self):
        self._commit()

    def rollback(self):
        self._rollback()

    def close(self):
        self._close()
