#!/usr/bin/env python3
# -*- coding: UTF-8 -*-
from typing import Union, Iterable

import pymysql.err
from addict import Dict
from pymysql import Connect
from pymysql.cursors import DictCursor, Cursor


class CursorCallType:
    FETCHONE = 1
    FETCHALL = 2
    LASTROWID = 3
    ROWCOUNT = 4
    DESCRIPTION = 5
    MESSAGES = 6
    ROWNUMBER = 7


class Database(object):
    def __init__(self, connect_args: Iterable = (), connect_kwargs: Union[dict, Dict] = {}, *args, **kwargs):
        self._connect_args: Iterable = connect_args
        self._connect_kwargs: Union[dict, Dict] = Dict(connect_kwargs)
        self._connect: Connect = None

    def open(self):
        self._connect_kwargs.setdefault("cursorclass", DictCursor)
        self._connect = Connect(*self._connect_args, **self._connect_kwargs)
        return isinstance(self._connect, Connect) and self._connect.open

    def close(self):
        if isinstance(self._connect, Connect) and self._connect.open:
            self._connect.close()
            return True
        return False

    def transaction(self, query_list: list = []) -> bool:
        try:
            cursor: Cursor = self._connect.cursor()
            self._connect.begin()
            for query in query_list:
                if isinstance(query, Union[tuple, list]):
                    cursor.execute(*query)
                if isinstance(query, dict):
                    cursor.execute(**query)
                if isinstance(query, str):
                    cursor.execute(query)
            self._connect.commit()
            return True
        except Exception as e:
            self._connect.rollback()
            raise e
        finally:
            cursor.close()

    def executemany(self, query: str = "", args: Iterable[object] = None):
        try:
            cursor: Cursor = self._connect.cursor()
            cursor.executemany(query=query, args=args)
            self._connect.commit()
            return cursor.rowcount
        except Exception as e:
            self._connect.rollback()
            raise e
        finally:
            cursor.close()

    def execute(self, query: str = "", args: Union[object, None] = None,
                cursor_call_type: int = CursorCallType.ROWCOUNT):
        try:
            cursor: Cursor = self._connect.cursor()
            cursor.execute(query=query, args=args)
            self._connect.commit()
            if cursor_call_type == CursorCallType.FETCHALL:
                return cursor.fetchall()
            elif cursor_call_type == CursorCallType.FETCHONE:
                return cursor.fetchone()
            elif cursor_call_type == CursorCallType.LASTROWID:
                return cursor.lastrowid
            elif cursor_call_type == CursorCallType.ROWCOUNT:
                return cursor.rowcount
            elif cursor_call_type == CursorCallType.DESCRIPTION:
                return cursor.description
            elif cursor_call_type == CursorCallType.MESSAGES:
                return cursor.messages
            elif cursor_call_type == CursorCallType.ROWNUMBER:
                return cursor.rownumber
            else:
                return cursor.rowcount
        except Exception as e:
            self._connect.rollback()
            raise e
        finally:
            cursor.close()

    def fetchone(self, query: str = "", args: Union[object, None] = None):
        return self.execute(query=query, args=args, cursor_call_type=CursorCallType.FETCHONE)

    def fetchall(self, query: str = "", args: Union[object, None] = None):
        return self.execute(query=query, args=args, cursor_call_type=CursorCallType.FETCHALL)

    def lastrowid(self, query: str = "", args: Union[object, None] = None):
        return self.execute(query=query, args=args, cursor_call_type=CursorCallType.LASTROWID)

    def rowcount(self, query: str = "", args: Union[object, None] = None):
        return self.execute(query=query, args=args, cursor_call_type=CursorCallType.ROWCOUNT)

    def description(self, query: str = "", args: Union[object, None] = None):
        return self.execute(query=query, args=args, cursor_call_type=CursorCallType.DESCRIPTION)

    def messages(self, query: str = "", args: Union[object, None] = None):
        return self.execute(query=query, args=args, cursor_call_type=CursorCallType.MESSAGES)

    def rownumber(self, query: str = "", args: Union[object, None] = None):
        return self.execute(query=query, args=args, cursor_call_type=CursorCallType.ROWNUMBER)
