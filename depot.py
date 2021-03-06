import socket
import signal as sig
import dumboard_config as cfg
import simplejson as json
import orchestra as orch
import requests as reqs
from flask import Flask, request
from contextlib import closing


def find_free_port():
    with closing(socket.socket(socket.AF_INET, socket.SOCK_STREAM)) as s:
        s.bind(('', 0))
        s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        return s.getsockname()[1]


def join_orchestra(conductor, member):
    url = 'http://localhost:' + str(conductor.port) + '/join/'
    reqs.post(url, data = member.toDict())


def leave_orchestra(conductor, member):
    url = 'http://localhost:' + str(conductor.port) + '/leave/'
    reqs.post(url, data = member.toDict())


def signal_handler(sig, frame):
    global conductor
    global member
    print("Leaving orchestra...")
    leave_orchestra(conductor, member)
    exit(0)


# Setting self up and registering with cconductor
sig.signal(sig.SIGINT, signal_handler)
conductor = orch.Conductor(cfg.conductor["port"])
member = orch.Member("Depot","depot", find_free_port(), conductor)

join_orchestra(conductor, member)


# Setting up server
app = Flask(__name__)

@app.route('/info/')
def welcome():
    global member
    return f"""<pre>
Member running on port {str(conductor.port)}
{str(member.toDict())}
</pre>
"""


@app.route('/store/', methods=['POST'])
def join():
    print("Received payload from " + str(request.json["member"]) + ", size = " + str(request.content_length) + " bytes")
    
    destination = request.json["member"]["name"] + "-" + request.json["member"]["section"] + ".json"
    print("Dumping to file " + destination)
    with open(destination, 'w') as outfile:
        json.dump(request.json, outfile)
    # print(request.json)
    return "OK"

if __name__ == '__main__':
    app.run(host="localhost", port=member.port)
