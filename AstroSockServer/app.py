from flask import Flask, render_template
import yaml
import socketserver
import sys
import os
from services.connect_demo import blueprint

app = Flask("AstroSock")

route_paths = []


def setup_services():
    stream = open("services.yaml", 'r')
    config = yaml.load(stream, yaml.Loader)
    services = []
    for service_name, args in config["services"].items():
        # Find a free port and run socket
        with socketserver.TCPServer(("localhost", 0), None) as s:
            free_port = s.server_address[1]
            module_name = "services." + args["name"]
            service_module = __import__(module_name, globals(), locals(), ['webservice'], 0)
            service_module.webservice.main(free_port)
            app.register_blueprint(blueprint, url_prefix="/service")
        args["port"] = free_port
        services.append(args)
    return services


active_services = setup_services()


@app.route("/")
def index():
    return render_template('index.html', services=active_services)
