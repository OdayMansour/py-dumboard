import dumboard_config as cfg
import simplejson as json
import orchestra as orch
from flask import Flask, request, jsonify


app = Flask(__name__)
orchestra = orch.Orchestra("dumboard")
conductor = orch.Conductor(cfg.conductor["port"])


@app.route('/')
def welcome():
  return 'Welcome to the conductor.'


@app.route('/info/')
def info():
    global orchestra
    members = ""
    for member in orchestra.members:
        members = members + member.toString() + "\n"
    return f"""<pre>
Conductor running on port {str(conductor.port)}
{members}
</pre>
"""


@app.route('/members/')
def members():
    global orchestra
    members = []
    for member in orchestra.members:
        members.append(member.toDict())
    return jsonify(members)


@app.route('/members/depot/')
def depot():
    global orchestra
    if orchestra.depot is not None:
        return jsonify(orchestra.depot.toDict())
    else:
        depot = orch.Member("", "", 0, orch.Conductor())
        for member in orchestra.members:
            if member.section == "depot":
                orchestra.setDepot(member)
        return jsonify(orchestra.depot.toDict())


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
    app.run(host="localhost", port=conductor.port, debug=False)
