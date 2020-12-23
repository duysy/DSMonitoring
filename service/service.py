import threading
import time
from threading import Thread
import os
import sqLine
from .ping import Ping
from .snmptrap import SnmpTrap
# import sys
# import os
# sys.path.append(os.path.abspath(os.path.join('..')))


class ClientThread(threading.Thread):
    def __init__(self, idHost, ipAddress):
        threading.Thread.__init__(self)
        self.ping = Ping()
        self.idHost = idHost
        self.ipAddress = ipAddress

    def run(self):
        time.sleep(5)
        sqline = sqLine.Sqline()
        if self.ping.ping(self.ipAddress):
            sqline.execute(
                "UPDATE host set activeAtatus = 1 where id = '{}'".format(self.idHost))
        else:
            sqline.execute(
                "UPDATE host set activeAtatus = 0 where id = '{}'".format(self.idHost))


class Service:
    def test(self):
        prosess = Thread(target=self.run, args=[])
        prosess.start()

    def run(self):
        while True:
            time.sleep(5)
            sqline = sqLine.Sqline()
            host = sqline.raw("SELECT * from host")
            for i in host:
                idHost = str(i[0])
                ipAddress = str(i[2])
                newthread = ClientThread(idHost, ipAddress)
                newthread.start()

    def discover(self, idHost):
        host = ""
        sqline = sqLine.Sqline()
        oids = sqline.raw("SELECT * from oid")
        hosts = sqline.raw("SELECT * from host WHERE id = '{}'".format(idHost))
        for host in hosts:
            host = host
        for oid in oids:
            snmptrap = SnmpTrap()  # self,ipAddress,idOid,communityName,port
            result = snmptrap.get(host[2], oid[2],  host[5], host[3])
            if(len(str(result)) != 0 or "No" not in str(result).split()):  # snmp oid not work
                listOid = str(host[8]).split(",") if len(str(host[8]).split(",")) > 0 else [host[8]]
                listOid = ",".join(listOid)
                # print(listOid)
                # print("UPDATE host set snmpOid = '{}' where id = '{}'".format(listOid,idHost))
                sqline = sqLine.Sqline()
                sqline.execute(
                    "UPDATE host set snmpOid = '{}' where id = '{}'".format(listOid, idHost))
            # print(oid[2])
# service = Service()
# service.discover("a03201b8-43ab-11eb-a0e9-f01faf2cabdc")
