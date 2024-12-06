#!/usr/bin/env python3
# -*- coding: UTF-8 -*-
import sqlite3
from _typeshed import SupportsLenAndGetItem
from sqlite3 import Connection, Cursor
from typing import Iterable, Union, Mapping

from addict import Dict
from typing_extensions import Buffer


class CursorCallType:
    FETCHONE = 1
    FETCHALL = 2
    LASTROWID = 3
    ROWCOUNT = 4
    DESCRIPTION = 5


class Database(object):
    def __init__(
            self,
            connect_args: Iterable = (),
            connect_kwargs: Union[dict, Dict] = {},
            *args,
            **kwargs
    ):
        self._connect_args: Iterable = connect_args
        self._connect_kwargs: Union[dict, Dict] = Dict(connect_kwargs)
        self._connect: Connection = None

    def open(self, row_factory=sqlite3.Row):
        self._connect = sqlite3.connect(*self.connect_args, **self.connect_kwargs.to_dict())
        self._connect.row_factory = row_factory
        return True

    def close(self) -> bool:
        if isinstance(self._connect, sqlite3.Connection):
            self._connect.close()
            return True
        return False

    def executescript(self, sql_script: str = "") -> int:
        try:
            cursor: Cursor = self._connect.cursor()
            cursor.executescript(sql_script)
            self._connect.commit()
            return cursor.rowcount
        except Exception as e:
            self._connect.rollback()
            raise e
        finally:
            cursor.close()

    def executemany(
            self,
            sql: str = "",
            seq_of_parameters: Iterable[
                SupportsLenAndGetItem[str | Buffer | int | float | None] | Mapping[
                    str, str | Buffer | int | float | None]
                ] = ()
    ) -> int:
        try:
            cursor: Cursor = self._connect.cursor()
            cursor.executemany(sql, seq_of_parameters)
            self._connect.commit()
            return cursor.rowcount
        except Exception as e:
            self._connect.rollback()
            raise e
        finally:
            cursor.close()

    def execute(
            self,
            sql: str = "",
            parameters: SupportsLenAndGetItem[str | Buffer | int | float | None] | Mapping[
                str, str | Buffer | int | float | None] = (),
            cursor_call_type: int = CursorCallType.ROWCOUNT
    ) -> int:
        try:
            cursor: Cursor = self._connect.cursor()
            cursor.execute(sql, parameters)
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
            else:
                return cursor.rowcount
        except Exception as e:
            self._connect.rollback()
            raise e
        finally:
            cursor.close()

    def rowcount(self, sql: str = "", parameters: SupportsLenAndGetItem[str | Buffer | int | float | None] | Mapping[
        str, str | Buffer | int | float | None] = ()):
        return self.execute(sql, parameters, cursor_call_type=CursorCallType.ROWCOUNT)

    def lastrowid(self, sql: str = "", parameters: SupportsLenAndGetItem[str | Buffer | int | float | None] | Mapping[
        str, str | Buffer | int | float | None] = ()):
        return self.execute(sql, parameters, cursor_call_type=CursorCallType.LASTROWID)

    def fetchall(self, sql: str = "", parameters: SupportsLenAndGetItem[str | Buffer | int | float | None] | Mapping[
        str, str | Buffer | int | float | None] = ()):
        return self.execute(sql, parameters, cursor_call_type=CursorCallType.FETCHALL)

    def fetchone(self, sql: str = "", parameters: SupportsLenAndGetItem[str | Buffer | int | float | None] | Mapping[
        str, str | Buffer | int | float | None] = ()):
        return self.execute(sql, parameters, cursor_call_type=CursorCallType.FETCHONE)
