from flask import Flask, render_template, session
import yaml
import socketserver
from multiprocessing import Process
import atexit
import publisher

app = Flask("AstroSock")
app.secret_key = "Change me for production!"

service_threads = []
active_services = []


def start_service(service_name, webservice_module):
    # Find a free port and run socket
    with socketserver.TCPServer(("localhost", 0), None) as s:
        free_port = s.server_address[1]
    print("Start service ", service_name)
    p = Process(target=webservice_module.run, args=[ free_port ])
    p.start()
    service_threads.append(p)
    print(service_name, "running")
    return free_port

def setup_services():
    stream = open("services.yaml", 'r')
    config = yaml.load(stream, yaml.Loader)
    
    for service_name, args in config["services"].items():
        module_name = "services." + service_name
        service_module = __import__(module_name, globals(), locals(), ['webservice', 'blueprint'], 0)
        port = start_service(service_name, service_module.webservice)
        app.register_blueprint(service_module.blueprint, url_prefix="/service/")
        args["port"] = port
        args["key"] = service_name
        active_services.append(args)


def exit_all_threads():
    for th in service_threads:
        th.join(2)
    print("All service threads are complete.")


@app.route("/")
def index():
    session['services'] = active_services
    return render_template('index.html', services=session['services'])


atexit.register(exit_all_threads)
setup_services()
