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
    command = 'python3 stress_cpu.py' # if you want to pass any arguments
    p = subprocess.Popen(
        [command],
        shell=True,
        stdin=None,
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        close_fds=True)
    out, err = p.communicate()
    return ""

@app.route('/', methods=['GET'])
def retrieve():
    print("GET Called")
    hostname = socket.gethostname()
    ip_address = socket.gethostbyname(hostname)
    return str(ip_address)

if __name__ == "__main__":
    app.run(host='0.0.0.0',port=5000)