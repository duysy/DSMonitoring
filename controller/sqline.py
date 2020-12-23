import sqlite3
class sqLine:
    def __init__(self):
        self.conn = sqlite3.connect("../db.db")
        self.c = self.conn.cursor()
        print("connect success")
    def execute(self,sql):
        self.c.execute(sql)
        self.conn.commit()
    def raw(self,sql):
        cursor  = self.conn.execute(sql)
        return cursor
    def test(self):
        print("dakjshfashfjaskfhafajkfhajshksjhfahskj")
# sqLine = sqLine()
# sqLine.execute("INSERT INTO host(id, hostName, snmpAddress, snmpPort, snmpCommunity, snmpDescription) VALUES ('{}', '{}', '{}', '{}', '{}', '{}')".format('id', 'hostName', 'snmpAddress', 'snmpPort', 'snmpCommunity', 'snmpDescription'))
