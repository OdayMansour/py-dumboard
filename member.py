import sys
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
    url = 'http://' + conductor.host + ':' + str(conductor.port) + '/join/'
    r = reqs.post(url, data = member.toDict())
    if r.status_code == 200:
        print("Successfully registered with the conductor.")
    else:
        print("Unsuccessfully registered with the conductor. Exiting.")
        exit(0)


def leave_orchestra(conductor, member):
    url = 'http://' + conductor.host + ':' + str(conductor.port) + '/leave/'
    reqs.post(url, data = member.toDict())


def signal_handler(sig, frame):
    global conductor
    global member
    print("Leaving orchestra...")
    leave_orchestra(conductor, member)
    exit(0)


# Setting self up and registering with cconductor
sig.signal(sig.SIGINT, signal_handler)
memberName = "Sample"
memberSection = "Misc"
if len(sys.argv) > 2:
    memberName = sys.argv[1]
    memberSection = sys.argv[2]
conductor = orch.Conductor(cfg.conductor["port"], cfg.conductor["host"])
member = orch.Member(memberName, memberSection, find_free_port(), socket.gethostname(), conductor)

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


if __name__ == '__main__':
    print(member.host)
    app.run(host=member.host, port=member.port)
