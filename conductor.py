import dumboard_config as cfg
import simplejson as json
import orchestra as orch
from flask import Flask
from flask import request


app = Flask(__name__)
orchestra = orch.Orchestra("dumboard")
conductor = orch.Conductor(cfg.conductor["port"])


@app.route('/')
def welcome():
  return 'Welcome to the conductor.'


@app.route('/info/')
def info():
    global orchestra
    json_members = ""
    for member in orchestra.members:
        json_members = json_members + str(member.toDict()) + "\n"
    return f"""<pre>
Conductor running on port {conductor.port}
{json_members}
</pre>
"""


@app.route('/join/', methods=['POST'])
def join():
    global orchestra
    member = orch.Member(request.form["name"], request.form["section"], int(request.form["port"]), conductor)
    if orchestra.addMember(member):
        return "OK"
    else:
        return "NOK"


@app.route('/leave/', methods=['POST'])
def leave():
    global orchestra
    member = orch.Member(request.form["name"], request.form["section"], int(request.form["port"]), conductor)
    if orchestra.removeMember(member):
        return "OK"
    else:
        return "NOK"


# Starting up server
if __name__ == '__main__':
    app.run(host="localhost", port=conductor.port, debug=True)
