import sqlite3
import time
class Sqline:
    def __init__(self):
        self.conn = sqlite3.connect("db.db")
        self.c = self.conn.cursor()
        # print("connect success")
    def execute(self,sql):
        self.c.execute(sql)
        self.conn.commit()
        self.conn.close()
    def raw(self,sql):
        with self.conn:
            cur = self.conn.cursor()
            cur.execute(sql)
            res = cur.fetchall()
        if self.conn:
            self.conn.close()
        return res
    def close(self):
        self.conn.close()

# sqline = sqLine()
# hosts = sqline.raw("SELECT * from host")
# for i in hosts:
#     print(i)
