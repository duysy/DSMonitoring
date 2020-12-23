import sqlite3
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
        cursor  = self.conn.execute(sql)
        # self.conn.close()
        return cursor

# sqline = sqLine()
# hosts = sqline.raw("SELECT * from host")
# for i in hosts:
#     print(i)
