from flask import Flask, render_template, request
from controller.configuration import Configuration
from controller.monitoring import Monitoring
from service.service import Service

app = Flask(__name__, static_url_path='/assets', static_folder='assets')

configuration = Configuration()
monitoring = Monitoring()
service = Service()


@app.route("/")
def dashboard():
    return render_template('dashboard.html')


@app.route("/add-host-snmp", methods=['GET', 'POST'])
def add_host_snmp():
    return configuration.add_host_snmp()


@app.route("/del-host-snmp", methods=['GET'])
def del_host_snmp():
    return configuration.del_host_snmp()

@app.route("/del-oid-snmp", methods=['GET'])
def del_oid_snmp():
    return configuration.del_oid_snmp()


@app.route("/host-discover", methods=['GET'])
def host_discover():
    return configuration.host_discover()


@app.route("/add-oid-snmp", methods=['GET', 'POST'])
def add_oid_snmp():
    return configuration.add_oid_snmp()


@app.route("/list-host-config", methods=['GET', 'POST'])
def list_host_config():
    return configuration.list_host_config()

@app.route("/list-oid-config")
def list_oid_config():
    return configuration.list_oid_config()

@app.route("/list-oid-host")
def list_oid_host():
    return configuration.list_oid_host()

@app.route("/add-host-oid-trigger", methods=['GET', 'POST'])
def add_host_oid_trigger():
    return configuration.add_host_oid_trigger()

    

@app.route("/list-host")
def list_host():
    return monitoring.list_host()


@app.route("/list-oid")
def list_oid():
    return monitoring.list_oid()




@app.route('/user/<username>')
def show_user_profile(username):
    return render_template('index.html', username=username)


@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        return 'About page'
    else:
        return 'About page'


if __name__ == "__main__":
    # service.start()
    app.run(host='0.0.0.0', debug=True)
