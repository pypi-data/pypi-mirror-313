"""
author: 馒头
email: neihanshenshou@163.com
"""
from pymysql.connections import Connection
from pymysql.cursors import DictCursor


class MySQL:

    def __init__(self, user="root", password="123456", database="mantou", host="127.0.0.1", port=3306, typo=DictCursor):
        self.conn = Connection(
            user=user,
            password=password,
            host=host,
            port=port,
            database=database,
            cursorclass=typo
        )

    def __enter__(self):
        return self

    def query(self, sql=None):
        cursor = self.conn.cursor()
        cursor.execute(query=sql or "select * from lick_dog")
        data = cursor.fetchall()
        cursor.close()
        return [each for each in data]

    def __exit__(self, exc_type, exc_val, exc_tb):
        self.conn.close()
