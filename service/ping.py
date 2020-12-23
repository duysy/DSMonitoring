import subprocess as sp
import sys
class Ping:
    def ping(self,ipAddress):
        if sys.platform.startswith('win'):
            status,result = sp.getstatusoutput("ping " + ipAddress)
        else:
            status,result = sp.getstatusoutput("ping -c1 -w2 " + ipAddress)
        if status == 0: 
            print("System " + ipAddress + " is UP !")
            return True
        else:
            print("System " + ipAddress + " is DOWN !")
            return False
# ping = Ping()
# ping.ping("127.0.0.1")