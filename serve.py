import flask
from flask import request, jsonify
import subprocess
import socket

app = flask.Flask(__name__)
# tell Flask to use the above defined config


# GET requests will be blocked 'GET', 
@app.route('/', methods=['POST'])
def save():
    print("POST Called")
    p = subprocess.Popen(["python3","stress_cpu.py"])
    return str(p.pid)

@app.route('/', methods=['GET'])
def retrieve():
    print("GET Called")
    hostname = socket.gethostname()
    ip_address = socket.gethostbyname(hostname)
    return str(ip_address)

if __name__ == "__main__":
    app.run(host='0.0.0.0',port=80)