from flask import Flask, render_template, request, redirect, jsonify, Response
import uuid
import time
import sqLine
from service.service import Service

service = Service()


class Api:
    def api_list_oid_host(self):
        id = request.args.get('id')
        sqline = sqLine.Sqline()
        oids = sqline.raw("SELECT oid.idOid,oid.name,oid.oid,oid.units,host_oid.value,host_oid.isWorking from host_oid INNER JOIN oid ON host_oid.idOid = oid.idOid WHERE host_oid.id='{}'".format(id))
        response = flask.jsonify({'some': oids[0][4]})
    	response.headers.add('Access-Control-Allow-Origin', '*')
    	return response

    def api_set_email_ping(self):
        return "hello"
