import subprocess as sp
import sys
from pysnmp.hlapi import *
class SnmpTrap:
    def get(self,ipAddress,idOid,communityName,port):
        errorIndication, errorStatus, errorIndex, varBinds = next(
        getCmd(SnmpEngine(),
        CommunityData(communityName),
        UdpTransportTarget((ipAddress,port)),
        ContextData(),
        ObjectType(ObjectIdentity(idOid)),#Internal Chassis Fan: Fan status
        )
        )
        varBind=""
        for varBind in varBinds:
            varBind = varBind
        return varBind
# snmpTrap = SnmpTrap()
# snmpTrap.get("127.0.0.1",'1.3.6.1.4.1.2021.10.1.3.1','vku',161)



