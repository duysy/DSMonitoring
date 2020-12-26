# import subprocess as sp
# class Ping:
#     def ping(self,ipAddress):
#         status,result = sp.getstatusoutput("ping -c1 -w2 " + ipAddress)
#         status1,result1 = sp.getstatusoutput("ping " + ipAddress)
#         if status1 == 0: 
#             print("System " + ipAddress + " is UP !")
#         else:
#             print("System " + ipAddress + " is DOWN !")
# ping = Ping()
# ping.ping("127.0.0.1")

import time
start_time = time.time()
print(start_time)
time.sleep(60*60)
print(time.time(),time.time() - start_time)