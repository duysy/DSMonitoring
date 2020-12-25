from flask import Flask, render_template, request
import sqLine


class Monitoring:
    def list_host(self):
        sqline = sqLine.Sqline()
        hosts = sqline.raw("SELECT * from host")
        return render_template('monitoring/list_host.html',hosts=hosts)
    def list_oid(self):
        sqline = sqLine.Sqline()
        oids = sqline.raw("SELECT * from oid")
        return render_template('monitoring/list_oid.html',oids=oids)
    def history_notification(self):
        sqline = sqLine.Sqline()
        history_notifications = sqline.raw("SELECT * from history_notification")
        return render_template('monitoring/history_notification.html',history_notifications=history_notifications)