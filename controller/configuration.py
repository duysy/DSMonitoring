from flask import Flask, render_template, request, redirect
import uuid
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

    def list_host_config(self):
        sqline = sqLine.Sqline()
        hosts = sqline.raw("SELECT * from host")
        return render_template('configuration/list_host.html', hosts=hosts)

    def host_discover(self):
        idHost = request.args.get('idHost')
        host = ""
        sqline = sqLine.Sqline()
        hosts = sqline.raw("SELECT * from host WHERE id = '{}'".format(idHost))
        for host in hosts:
            host = host
        service.discover(idHost)
        return redirect("/list-host-config")
