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
from typing import Iterable, Union

from pymysql import Connection, DatabaseError
from pymysql.cursors import DictCursor


class Database(object):
    """
    pymysql database class

    @see https://pymysql.readthedocs.io/en/latest/
    """

    def __init__(
            self,
            connect_kwargs: dict = None,
    ):
        """
        pymysql database class
        :param connect_kwargs: @see https://pymysql.readthedocs.io/en/latest/modules/connections.html#pymysql.connections.Connection
        """
        self.connect_kwargs = connect_kwargs if isinstance(connect_kwargs, dict) else {}
        self.connect_kwargs.setdefault("cursorclass", DictCursor)
        self.connect: Connection = None

    def open(self):
        """
        connect open
        :return:
        """
        self.connect = Connection(**self.connect_kwargs)
        return isinstance(self.connect, Connection) and self.connect.open

    def close(self):
        """
        connect close
        :return:
        """
        if isinstance(self.connect, Connection) and self.connect.open:
            self.connect.close()
            return True
        return False

    def executemany(
            self,
            query: str,
            args: Iterable[object],
    ):
        """
        connect cursor executemany
        :param query:
        :param args:
        :return:
        """
        with self.connect.cursor() as cursor:
            cursor.executemany(query=query, args=args)
            self.connect.commit()
            return cursor.rowcount

    def execute(
            self,
            query: str,
            args: object,
    ):
        """
        connect cursor execute
        :param query:
        :param args:
        :return:
        """
        with self.connect.cursor() as cursor:
            cursor.execute(query=query, args=args)
            self.connect.commit()
            return cursor.rowcount

    def fetchone(
            self,
            query: str,
            args: object,
    ):
        """
        connect cursor fetchone
        :param query:
        :param args:
        :return:
        """
        with self.connect.cursor() as cursor:
            cursor.execute(query=query, args=args)
            self.connect.commit()
            return cursor.fetchone()

    def fetchall(
            self,
            query: str,
            args: object = None,
    ):
        """
        connect cursor fetchall
        :param query:
        :param args:
        :return:
        """
        with self.connect.cursor() as cursor:
            cursor.execute(query=query, args=args)
            self.connect.commit()
            return cursor.fetchall()

    def fetchmany(
            self,
            query: str,
            args: object,
            size: int = None,
    ):
        """
        connect cursor fetchmany
        :param query:
        :param args:
        :param size:
        :return:
        """
        with self.connect.cursor() as cursor:
            cursor.execute(query=query, args=args)
            self.connect.commit()
            return cursor.fetchmany(size=size)

    def rowcount(
            self,
            query: str,
            args: object = None,
    ):
        """
        connect cursor rowcount
        :param query:
        :param args:
        :return:
        """
        with self.connect.cursor() as cursor:
            cursor.execute(query=query, args=args)
            self.connect.commit()
            return cursor.rowcount

    def lastrowid(
            self,
            query: str,
            args: object = None,
    ):
        """
        connect cursor lastrowid
        :param query:
        :param args:
        :return:
        """
        with self.connect.cursor() as cursor:
            cursor.execute(query=query, args=args)
            self.connect.commit()
            return cursor.lastrowid

    def description(
            self,
            query: str,
            args: object = None,
    ):
        """
        connect cursor description
        :param query:
        :param args:
        :return:
        """
        with self.connect.cursor() as cursor:
            cursor.execute(query=query, args=args)
            self.connect.commit()
            return cursor.description

    def transaction(self, query_list: Union[tuple, list] = None):
        """
        connect cursor transaction
        :param query_list:
        :return:
        """
        query_list = query_list if isinstance(query_list, (tuple, list)) else []
        with self.connect.cursor() as cursor:
            try:
                self.connect.begin()
                for query in query_list:
                    if isinstance(query, Union[tuple, list]):
                        cursor.execute(*query)
                    if isinstance(query, dict):
                        cursor.execute(**query)
                    if isinstance(query, str):
                        cursor.execute(query=query)
                self.connect.commit()
                return True
            except Exception as e:
                self.connect.rollback()
                raise e
            finally:
                cursor.close()
