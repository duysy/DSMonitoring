import threading
import time
import uuid
from threading import Thread
import os
import sqLine
from .ping import Ping
from .snmptrap import SnmpTrap
from .smtpemail import SmtpEmail
# import sys
# import os
# sys.path.append(os.path.abspath(os.path.join('..')))


class ClientThread(threading.Thread):
    def __init__(self, host):
        threading.Thread.__init__(self)
        self.ping = Ping()
        self.host = host

    def getValueOid(self):
        sqline = sqLine.Sqline()
        host_oid = sqline.raw("SELECT host_oid.id,oid.oid from host_oid INNER JOIN oid ON host_oid.idOid = oid.idOid WHERE host_oid.idHost='{}'".format(self.host[0]))
        for oid in host_oid:
            snmptrap = SnmpTrap()# self,ipAddress,idOid,communityName,port
            result = snmptrap.get(self.host[2], oid[1], self.host[5], self.host[3])
            if(self.oidIsWorking(result)):  # snmp oid not work
                value = str(result).split("=")[1].replace(" ", "")
                sqline = sqLine.Sqline()
                sqline.execute("UPDATE host_oid SET value = '{}' WHERE id = '{}' ;".format(value, oid[0]))
                idHostOid=oid[0]
                self.checkTrigger(idHostOid)

    def checkTrigger(self,idHostOid):
        sqline = sqLine.Sqline()
        host_oid = sqline.raw("SELECT host_oid.id,oid.idOid,oid.name,oid.oid,oid.units,host_oid.value,host_oid.isWorking from host_oid INNER JOIN oid ON host_oid.idOid = oid.idOid WHERE host_oid.id='{}'".format(idHostOid))
        sqline = sqLine.Sqline()
        trigger = sqline.raw("SELECT * from trigger WHERE idHostOid='{}'".format(idHostOid))
        valueOidHost = host_oid[0][5]
        if len(trigger) > 0: 
            solve = eval(str(trigger[0][3]).replace("[[value]]",str(valueOidHost))) # return rule in trigger
            print(host_oid[0][0],solve)
            lastTimeTrigger = int(trigger[0][4])
            idTrigger=trigger[0][0]
            if(solve and time.time() - lastTimeTrigger > 1000):
                sqline = sqLine.Sqline()
                sqline.execute("UPDATE trigger SET lastTime = '{}' WHERE id = '{}' ;".format(time.time(), idTrigger))
                sqline = sqLine.Sqline()
                notification = sqline.raw("SELECT * from notification WHERE id='{}'".format(str(trigger[0][2]))) #get info about notification
                nameOid = host_oid[0][2]
                valueOidHost = host_oid[0][5]
                emailAddress = notification[0][4]
                passwork = notification[0][5]
                toEmail = notification[0][6]
                print(nameOid,valueOidHost,emailAddress,passwork,toEmail)
                smtpemail =SmtpEmail(emailAddress,passwork)
                if(smtpemail.sendEmail(toEmail,nameOid,valueOidHost)):
                    id = uuid.uuid1()
                    sqline = sqLine.Sqline()
                    sqline.execute("INSERT INTO history_notification(id,nameProblem,content,time) VALUES ('{}', '{}', '{}','{}')".format(id,nameOid, valueOidHost,time.time()))

    def oidIsWorking(self, result):
        if("No" not in str(result).split() and len(str(result))>0):
            return True
        return False
    def run(self):
        time.sleep(5)
        if self.ping.ping(self.host[2]):
            sqline = sqLine.Sqline()
            sqline.execute("UPDATE host set activeAtatus = 1 where id = '{}'".format(self.host[0]))
            self.getValueOid()
        else:
            sqline = sqLine.Sqline()
            host = sqline.raw("SELECT * from host WHERE id='{}'".format(idHostOid))
            lastTimeHost = host[0][8]
            if time.time() - lastTimeHost > 1000:
                emailAddress = "duysyduysyduysy1@gmail.com"
                passwork = "1h3j6n3j8l9n5k2h6j"
                toEmail = "duyduysysy@gmail.com"
                subject= "Cant connect to host"
                content = "Cant connect to host with :{}".format(str(host[0]))
                print(emailAddress,passwork,toEmail)
                smtpemail =SmtpEmail(emailAddress,passwork)
                if(smtpemail.sendEmail(toEmail,subject,content)):
                    id = uuid.uuid1()
                    sqline = sqLine.Sqline()
                    sqline.execute("INSERT INTO history_notification(id,nameProblem,content,time) VALUES ('{}', '{}', '{}','{}')".format(id,subject, content,time.time()))

                    sqline = sqLine.Sqline()
                    sqline.execute("UPDATE host set activeAtatus = 0 , lastTime='{}' where id = '{}'".format(time.time(),self.host[0]))


class Service:
    def start(self):
        print("Start service")
        prosess = Thread(target=self.run, args=[])
        prosess.start()
    def run(self):
        while True:
            time.sleep(5)
            sqline = sqLine.Sqline()
            hosts = sqline.raw("SELECT * from host")
            for host in hosts:
                newthread = ClientThread(host)
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
                sqline.execute("INSERT INTO host_oid (id,idHost, idOid, value,isWorking) VALUES ( '{}','{}', '{}', '{}',{})".format(id, idHost, oid[0], value, 1))

    def oidIsWorking(self, result):
        if("No" not in str(result).split() and len(str(result))>0):
            return True
        return False


# service = Service()
# service.discover("a03201b8-43ab-11eb-a0e9-f01faf2cabdc")
