# python操作sqlite的简单封装，具体使用见__main__代码块
import os
import random
import sqlite3
import sys
from typing import List

from tooly.types import Literal


class Column:
    def __init__(self, colName: str,
                 colType: Literal["text", "integer"],
                 unique=False,
                 length=256,
                 notNull=False):
        """
        列属性
        :param unique: 唯一性约束
        :param length: 字符串默认256，int默认4
        :param notNull: 空约束
        """
        self.colType = colType
        self.colName = colName
        self.unique = unique
        self.length = length

        if colType == "integer":
            if length > 8:
                self.length = 4
            elif self.length > 4:
                self.length = 8
        self.notNull = notNull
        if colName == "id":
            self.notNull = True

    def getFieldDef(self):
        notNull = ""
        if self.notNull:
            notNull = " not null"
        return f'\n\t"{self.colName}" {self.colType}({self.length}){notNull},'

    def getUniqueDef(self):
        if not self.unique:
            return ""
        return f',\n\tCONSTRAINT "{self.colName}" UNIQUE ("{self.colName}")'


class Db:
    def __init__(self, fname: str, showSql=True):
        self.conn = sqlite3.connect(fname)
        self.__showSql = showSql

    def _showSql(self, sql, args):
        if not self.__showSql:
            return
        frame = sys._getframe(2)
        fname = os.path.basename(frame.f_code.co_filename)
        line = frame.f_lineno

        sql = sql.strip()

        for arg in args:
            if isinstance(arg, str):
                sql = sql.replace("?", '"' + arg + '"', 1)
            else:
                sql = sql.replace("?", str(arg), 1)

        print(f"[{fname}:{line}] {sql}")

    def execute(self, sql: str, args=(), autoCommit: bool = True):
        """
        执行sql语句（不返回任何结果)
        """
        self._showSql(sql, args)
        self.conn.execute(sql, args)
        if autoCommit:
            self.conn.commit()

    def query(self, sql: str, args=()):
        """
        查询sql
        """
        self._showSql(sql, args)
        cursor = self.conn.execute(sql, args)
        try:
            ret = [i for i in cursor.fetchall()]
            ret.insert(0, [k[0] for k in cursor.description])
            return ret
        finally:
            cursor.close()

    def insertDict(self, tableName: str, obj: dict, autoCommit=True):
        """
        插入一行数据，根据kv结果自动插入
        """
        keys = [k for k in obj.keys()]
        keyNames = ", ".join(keys)
        place = ', '.join(['?' for k in keys])

        sql = f"insert into {tableName} ({keyNames}) values ({place})"
        vals = [obj[k] for k in keys]

        self._showSql(sql, vals)

        self.conn.execute(sql, vals)

        if autoCommit:
            self.conn.commit()

    def close(self):
        self.conn.close()

    def createTable(self, tableName: str, cols: List[Column]):
        """
        创建数据库
        """
        sql = f"""create table if not exists "{tableName}" ("""
        for col in cols:
            sql += col.getFieldDef()
        sql += '\n\tPRIMARY KEY ("id")'
        for col in cols:
            sql += col.getUniqueDef()
        sql += ");"

        self._showSql(sql, ())
        self.conn.execute(sql)


if __name__ == '__main__':
    # 连接数据库
    db = Db("test.db")

    # 创建数据库表
    db.createTable("user", [
        Column("id", "text"),
        Column("name", "text", unique=True),
        Column("age", "integer"),
        Column("address", "text"),
        Column("sex", "text")
    ])

    # 插入数据
    db.insertDict("user", {
        "id": f"id{random.randint(0, 10000):05d}",
        "age": 12,
        "name": f"张三{random.randint(0, 10000):05d}",
        "sex": "男",
        "address": "时代发生的开发建设快递分拣"
    })

    # 查询数据
    data = db.query("select * from user")
    print(data)

    db.insertDict("user", {
        "id": f"id{random.randint(0, 10000):05d}",
        "age": 12,
        "name": f"张三",
        "sex": "男",
        "address": "时代发生的开发建设快递分拣"
    })
    db.insertDict("user", {
        "id": f"id{random.randint(0, 10000):05d}",
        "age": 12,
        "name": f"张三",
        "sex": "男",
        "address": "时代发生的开发建设快递分拣"
    })
