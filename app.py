from flask import Flask, render_template, request
import socket
from concurrent.futures import ThreadPoolExecutor

app = Flask(__name__)

def scan_port(target, port):
    try:
        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        s.settimeout(0.5)
        result = s.connect_ex((target, port))
        s.close()
        if result == 0:
            return port
    except:
        return None

def scan_ports(target, start_port, end_port):
    open_ports = []
    with ThreadPoolExecutor(max_workers=100) as executor:
        results = executor.map(lambda p: scan_port(target, p), range(start_port, end_port+1))
    for r in results:
        if r:
            open_ports.append(r)
    return open_ports

@app.route("/", methods=["GET", "POST"])
def index():
    open_ports = []
    error = None

    if request.method == "POST":
        try:
            target = request.form["target"]
            start_port = int(request.form["start_port"])
            end_port = int(request.form["end_port"])
            open_ports = scan_ports(target, start_port, end_port)
        except:
            error = "Қате енгізу!"

    return render_template("index.html", open_ports=open_ports, error=error)

if __name__ == "__main__":
    app.run(debug=True)
