from flask import Flask, render_template, request, redirect
import uuid
import time
import sqLine
from service.service import Service

service = Service()


class Configuration:
    def add_host_snmp(self):
        if request.method == 'POST':
            id = uuid.uuid1()
            hostName = request.form['hostName']
            snmpAddress = request.form['snmpAddress']
            snmpPort = request.form['snmpPort']
            snmpCommunity = request.form['snmpCommunity']
            snmpDescription = request.form['snmpDescription']
            sqline = sqLine.Sqline()
            sqline.execute("INSERT INTO host(id, hostName, snmpAddress, snmpPort, available , snmpCommunity, snmpDescription) VALUES ('{}', '{}', '{}', '{}', '{}','{}', '{}')".format(
                id, hostName, snmpAddress, snmpPort, "SNMP", snmpCommunity, snmpDescription))
            return redirect("/list-host")
        else:
            return render_template('configuration/add_host_snmp.html')

    def list_host_config(self):
        sqline = sqLine.Sqline()
        hosts = sqline.raw("SELECT * from host")
        host_=[]
        for host in hosts:
            sqline = sqLine.Sqline()
            oid = sqline.raw("SELECT count(idOid) from host_oid where idHost = '{}'".format(host[0]))
            host_.append([host[0],host[1],host[2],host[3],host[4],host[5],host[6],"",oid[0][0]])
        return render_template('configuration/list_host.html', hosts=host_)

    def del_host_snmp(self):
        if request.method == 'GET':
            idHost = request.args.get('idHost')
            sqline = sqLine.Sqline()
            sqline.execute("DELETE FROM host WHERE id = '{}'".format(idHost))
            return redirect("list-host-config")

#######################################################################################################
    def add_oid_snmp(self):
        if request.method == 'POST':
            id = uuid.uuid1()
            name = request.form['name']
            oid = request.form['oid']
            units = request.form['units']
            description = request.form['description']
            sqline = sqLine.Sqline()
            sqline.execute("INSERT INTO oid (idoid, name, oid, units, description) VALUES ( '{}', '{}', '{}', '{}','{}')".format(
                id, name, oid, units, description))
            return redirect("/list-host")
        else:
            return render_template('configuration/add_oid_snmp.html')

    def list_oid_config(self):
        sqline = sqLine.Sqline()
        oids = sqline.raw("SELECT * from oid")
        return render_template('configuration/list_oid.html', oids=oids)

    def del_oid_snmp(self):
        if request.method == 'GET':
            idOid = request.args.get('idOid')
            sqline = sqLine.Sqline()
            sqline.execute("DELETE FROM oid WHERE idOid = '{}'".format(idOid))
            return redirect("list-oid-config")

#######################################################################################################

    def host_discover(self):
        idHost = request.args.get('idHost')
        host = ""
        sqline = sqLine.Sqline()
        hosts = sqline.raw("SELECT * from host WHERE id = '{}'".format(idHost))
        for host in hosts:
            host = host
        # try:
        #     service.discover(idHost)
        # except:
        #     return "Please check Oid"
        service.discover(idHost)
        return redirect("/list-host-config")

    def list_oid_host(self):
        idHost = request.args.get('idHost')
        sqline = sqLine.Sqline()
        oids = sqline.raw("SELECT host_oid.id,oid.idOid,oid.name,oid.oid,oid.units,host_oid.value,host_oid.isWorking from host_oid INNER JOIN oid ON host_oid.idOid = oid.idOid WHERE host_oid.idHost='{}'".format(idHost))
        for i in oids:
            print("dsadasdas",i)
        return render_template('configuration/list_oid_host.html', oids=oids)

    def add_host_oid_trigger(self):
        if request.method == 'POST':
            id = uuid.uuid1()
            idHostOid = request.form['idHostOid']
            notification = request.form['notification']
            trigger = request.form['trigger']
            sqline = sqLine.Sqline()
            print(id,idHostOid,trigger)
            sqline.execute("INSERT INTO trigger(id,idHostOid,notification,trigger,lastTime) VALUES ('{}', '{}', '{}','{}','{}')".format(id,idHostOid, notification,trigger,time.time()))
            return redirect("/list-host-config")
        else:
            idHostOid = request.args.get('idHostOid')
            sqline = sqLine.Sqline()
            notifications = sqline.raw("SELECT * from notification")
            return render_template('configuration/add_host_oid_trigger.html',idHostOid=idHostOid,notifications=notifications)
###############################################################################################
    def add_notification(self):
        if request.method == 'POST':
            id = uuid.uuid1()
            name = request.form['name']
            type_ = request.form['type']
            content = request.form['content']
            emailaddress = request.form['emailaddress']
            password = request.form['password']
            toemail = request.form['toemail']
            sqline = sqLine.Sqline()
            sqline.execute("INSERT INTO notification(id,name,type,content,emailAddress,passwork,toEmail) VALUES ('{}', '{}', '{}','{}', '{}', '{}','{}')".format(id,name,type_,content,emailaddress,password,toemail))
            return redirect("/list-notification")
        else:
            return render_template('configuration/add_notification.html')
    def del_notification(self):
        if request.method == 'GET':
            id = request.args.get('id')
            sqline = sqLine.Sqline()
            sqline.execute("DELETE FROM notification WHERE id = '{}'".format(id))
            return redirect("/list-notification")

