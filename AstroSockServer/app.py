from flask import Flask, render_template
import yaml
import socketserver
import threading
import atexit

app = Flask("AstroSock")

service_threads = []


def setup_services():
    stream = open("services.yaml", 'r')
    config = yaml.load(stream, yaml.Loader)
    services = []
    for service_name, args in config["services"].items():
        # Find a free port and run socket
        with socketserver.TCPServer(("localhost", 0), None) as s:
            free_port = s.server_address[1]
        module_name = "services." + args["name"]
        service_module = __import__(module_name, globals(), locals(), ['webservice', 'blueprint'], 0)
        print("Start service ", service_name)
        th = threading.Thread(target=service_module.webservice.run, args=[free_port])
        th.start()
        service_threads.append(th)
        print(service_name, "running")
        app.register_blueprint(service_module.blueprint, url_prefix="/service")
        args["port"] = free_port
        services.append(args)
    return services


active_services = setup_services()

def exit_all_threads():
    for th in service_threads:
        th.join()
    print("All service threads are complete.")


@app.route("/")
def index():
    return render_template('index.html', services=active_services)


atexit.register(exit_all_threads)
