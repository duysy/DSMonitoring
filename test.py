import subprocess as sp
class Ping:
    def ping(self,ipAddress):
        status,result = sp.getstatusoutput("ping -c1 -w2 " + ipAddress)
        status1,result1 = sp.getstatusoutput("ping " + ipAddress)
        if status1 == 0: 
            print("System " + ipAddress + " is UP !")
        else:
            print("System " + ipAddress + " is DOWN !")
ping = Ping()
ping.ping("127.0.0.1")