import dumboard_config as cfg
import simplejson as json
from flask import Flask
from flask import request

app = Flask(__name__)


# Setting up orchestra
class Orchestra:
    members = []


class Member:
    name = ""
    type = ""


orchestra = Orchestra()

# Starting up server
if __name__ == '__main__':
    app.run(host="localhost", port=cfg.conductor["port"], debug=True)


@app.route('/')
def welcome():
  return 'Welcome to the conductor.'


@app.route('/info/')
def info():
  global orchestra
  return f"""<pre>
Conductor running on port {cfg.conductor["port"]} <br />
{json.dumps(orchestra.members, sort_keys=True, indent=4 * ' ')}
</pre>
"""


@app.route('/join/', methods=['POST'])
def join():
    global orchestra

    member = {
        "name": request.form["name"],
        "type": request.form["type"]
        }

    if member not in orchestra.members:
        orchestra.members.append(member)
        return "OK"
    else:
        return "NOK - Already registered"

    orchestra.members.append()
    return "OK"


@app.route('/leave/', methods=['POST'])
def leave():
    member = {
        "name": request.form["name"],
        "type": request.form["type"]
        }
    if member in orchestra.members:
        orchestra.members.remove(member)
        return "OK"
    else:
        return "NOK - Not registered"
