#!/usr/bin/env python3
# -*- coding: UTF-8 -*-
"""
=================================================
作者：[郭磊]
手机：[15210720528]
Email：[174000902@qq.com]
Github：https://github.com/guolei19850528/py3_database
=================================================
"""
import sqlite3


class Database(object):
    """
    sqlite3 database class

    @see https://docs.python.org/zh-cn/3.12/library/sqlite3.html#
    """

    def __init__(self, connect_kwargs=None):
        """
        sqlite3 database class
        :param connect_kwargs: @see https://docs.python.org/zh-cn/3.12/library/sqlite3.html#sqlite3.connect
        """
        self.connect_kwargs = connect_kwargs if isinstance(connect_kwargs, dict) else {}
        self.connect: sqlite3.Connection = None

    def open(self, row_factory=sqlite3.Row):
        row_factory = row_factory if row_factory is not None else sqlite3.Row
        self.connect = sqlite3.connect(**self.connect_kwargs)
        self.connect.row_factory = row_factory
        return True

    def close(self) -> bool:
        if isinstance(self.connect, sqlite3.Connection):
            self.connect.close()
            return True
        return False

    def executescript(self, sql_script: str):
        try:
            cursor = self.connect.cursor()
            cursor.executescript(sql_script)
            self.connect.commit()
            return cursor.rowcount
        except Exception as e:
            self.connect.rollback()
            raise e
        finally:
            cursor.close()

    def executemany(self, sql: str, seq_of_parameters=None):
        try:
            cursor = self.connect.cursor()
            cursor.executemany(sql, seq_of_parameters)
            self.connect.commit()
            return cursor.rowcount
        except Exception as e:
            self.connect.rollback()
            raise e
        finally:
            cursor.close()

    def execute(self, sql: str, parameters=()):
        try:
            cursor = self.connect.cursor()
            cursor.execute(sql, parameters)
            self.connect.commit()
            return cursor.rowcount
        except Exception as e:
            self.connect.rollback()
            raise e
        finally:
            cursor.close()

    def fetchone(self, sql: str, parameters=()):
        try:
            cursor = self.connect.cursor()
            cursor.execute(sql, parameters)
            self.connect.commit()
            return cursor.fetchone()
        except Exception as e:
            self.connect.rollback()
            raise e
        finally:
            cursor.close()

    def fetchall(self, sql: str, parameters=()):
        try:
            cursor = self.connect.cursor()
            cursor.execute(sql, parameters)
            self.connect.commit()
            return cursor.fetchall()
        except Exception as e:
            self.connect.rollback()
            raise e
        finally:
            cursor.close()

    def fetchmany(self, size, sql: str, parameters=()):
        try:
            cursor = self.connect.cursor()
            cursor.execute(sql, parameters)
            self.connect.commit()
            return cursor.fetchmany(size=size)
        except Exception as e:
            self.connect.rollback()
            raise e
        finally:
            cursor.close()

    def rowcount(self, sql: str, parameters=()):
        try:
            cursor = self.connect.cursor()
            cursor.execute(sql, parameters)
            self.connect.commit()
            return cursor.rowcount
        except Exception as e:
            self.connect.rollback()
            raise e
        finally:
            cursor.close()

    def lastrowid(self, sql: str, parameters=()):
        try:
            cursor = self.connect.cursor()
            cursor.execute(sql, parameters)
            self.connect.commit()
            return cursor.lastrowid
        except Exception as e:
            self.connect.rollback()
            raise e
        finally:
            cursor.close()

    def description(self, sql: str, parameters=()):
        try:
            cursor = self.connect.cursor()
            cursor.execute(sql, parameters)
            self.connect.commit()
            return cursor.description
        except Exception as e:
            self.connect.rollback()
            raise e
        finally:
            cursor.close()
