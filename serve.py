import flask
from flask import request, jsonify
from stress_cpu import *
import subprocess
import socket

config = {
    "DEBUG": False,          # some Flask specific configs
    "CACHE_TYPE": "SimpleCache"  # Flask-Caching related configs
}

# Do intensive computation to stress the CPU
def stress_cpu(n):
    total = 0
    for i in range(n):
        total += i**2
    return total

app = flask.Flask(__name__)
# tell Flask to use the above defined config
app.config.from_mapping(config)

# GET requests will be blocked 'GET', 
@app.route('/', methods=['POST'])
def save():
    command = './stress_cpu.py' # if you want to pass any arguments
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
    return str(socket.gethostname())