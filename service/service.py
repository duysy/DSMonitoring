import threading
import time
import uuid
from threading import Thread
import os
import sqLine
from .ping import Ping
from .snmptrap import SnmpTrap
# import sys
# import os
# sys.path.append(os.path.abspath(os.path.join('..')))


class ClientThread(threading.Thread):
    def __init__(self, host, ipAddress):
        threading.Thread.__init__(self)
        self.ping = Ping()
        self.host = host

    def getValueOid(self, host):
        sqline = sqLine.Sqline()
        oids = sqline.raw("SELECT host_oid.id from host_oid INNER JOIN oid ON host_oid.idOid = oid.idOid WHERE host_oid.idHost='{}'".format(host[0]))
        for oid in oids:
            snmptrap = SnmpTrap()# self,ipAddress,idOid,communityName,port
            result = snmptrap.get(host[2], oid[2],  host[5], host[3])
            if(not self.oidIsWorking(result)):  # snmp oid not work
                value = 'str(result).split("=")[1].replace(" ", "")'
                sqline = sqLine.Sqline()
                sqline.execute("UPDATE host_oid SET value = '{}' WHERE id = '{}' ;".format(value, oid[0]))
    def run(self):
        time.sleep(5)
        if self.ping.ping(self.host[2]):
            sqline = sqLine.Sqline()
            sqline.execute("UPDATE host set activeAtatus = 1 where id = '{}'".format(self.idHost))
            getValueOid(self.host)
        else:
            sqline.execute("UPDATE host set activeAtatus = 0 where id = '{}'".format(self.idHost))


class Service:
    def start(self):
        print("Start service")
        prosess = Thread(target=self.run, args=[])
        prosess.start()

    def run(self):
        while True:
            time.sleep(5)
            sqline = sqLine.Sqline()
            host = sqline.raw("SELECT * from host")
            for i in host:
                newthread = ClientThread(host, ipAddress)
                newthread.start()

    

    def discover(self, idHost):
        host = ""
        sqline = sqLine.Sqline()
        oids = sqline.raw("SELECT * from oid")
        sqline = sqLine.Sqline()
        hosts = sqline.raw("SELECT * from host WHERE id = '{}'".format(idHost))
        sqline = sqLine.Sqline()
        sqline.execute("DELETE FROM host_oid WHERE idHost = '{}'".format(
            idHost))  # delete all item from host_oid
        for host in hosts:
            host = host
        for oid in oids:
            snmptrap = SnmpTrap()  # self,ipAddress,idOid,communityName,port
            result = snmptrap.get(host[2], oid[2],  host[5], host[3])
            if(self.oidIsWorking(result)):  # snmp oid not work
                value = str(result).split("=")[1].replace(" ", "")
                sqline = sqLine.Sqline()
                id = uuid.uuid1()
                sqline.execute("INSERT INTO host_oid (id,idHost, idOid, value,isWorking) VALUES ( '{}','{}', '{}', '{}',{})".format(
                    id, idHost, oid[0], value, 1))

    def oidIsWorking(self, result):
        if("No" not in str(result).split() and len(result)>0):
            return True
        return False


# service = Service()
# service.discover("a03201b8-43ab-11eb-a0e9-f01faf2cabdc")
