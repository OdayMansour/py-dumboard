import socket, sched, time, threading
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
member = orch.Member("OpenWeatherMap","fetcher", find_free_port(), conductor)
depot = None

join_orchestra(conductor, member)


# Setting up server
app = Flask(__name__)

@app.route('/info/')
def welcome():
    global member
    return f"""<pre>
Member running on port {str(conductor.port)}
{str(member.toDict())}

Config: 
{cfg.openweathermap}
</pre>
"""


# Generic fetching
def getDepot():
    global depot
    if depot is None:
        print("Getting the depot")
        url = 'http://localhost:' + str(conductor.port) + '/members/depot/'
        response = reqs.get(url).json()
        depot = orch.Member(response["name"], response["section"], response["port"], conductor)
    return depot


def fetch_and_send():
    fetchedDocument = orch.FetchedDocument(fetch(),member)
    store(fetchedDocument)


def store(fetchedDocument):
    print("Storing document (" + str(len(str(fetchedDocument.document))) + " bytes) from " + str(fetchedDocument.member.toDict()) + " at " + str(fetchedDocument.timestamp))
    depot = getDepot()
    print("Sending it to " + depot.toString())
    url = 'http://localhost:' + str(depot.port) + '/store/'
    print(fetchedDocument.toDict())
    reqs.post(url, json = fetchedDocument.toDict())


# Custom fetching
def fetch():
    request_url = cfg.openweathermap["url"]
    request_url = request_url.replace("__APIKEY__", cfg.openweathermap["apikey"])
    request_url = request_url.replace("__APIPARAMS__", cfg.openweathermap["apiparams"])
    print("Requesting:")
    # print(request_url)
    # response = reqs.get(request_url)
    # print(response.status_code)
    # response = {"lat":51.47,"lon":-0.02,"timezone":"Europe/London","current":{"dt":1586202001,"sunrise":1586150592,"sunset":1586198470,"temp":285.09,"feels_like":282.89,"pressure":1024,"humidity":62,"dew_point":278.05,"uvi":3.82,"clouds":6,"visibility":10000,"wind_speed":1.5,"wind_deg":0,"weather":[{"id":800,"main":"Clear","description":"clear sky","icon":"01n"}],"rain":{}},"hourly":[{"dt":1586199600,"temp":285.09,"feels_like":282.4,"pressure":1024,"humidity":62,"dew_point":278.05,"clouds":6,"wind_speed":2.2,"wind_deg":276,"weather":[{"id":800,"main":"Clear","description":"clear sky","icon":"01n"}]},{"dt":1586203200,"temp":285.19,"feels_like":282.57,"pressure":1025,"humidity":59,"dew_point":277.43,"clouds":4,"wind_speed":1.94,"wind_deg":274,"weather":[{"id":800,"main":"Clear","description":"clear sky","icon":"01n"}]},{"dt":1586206800,"temp":285.08,"feels_like":282.37,"pressure":1026,"humidity":58,"dew_point":277.09,"clouds":3,"wind_speed":1.97,"wind_deg":278,"weather":[{"id":800,"main":"Clear","description":"clear sky","icon":"01n"}]},{"dt":1586210400,"temp":284.66,"feels_like":282.08,"pressure":1027,"humidity":60,"dew_point":277.17,"clouds":2,"wind_speed":1.8,"wind_deg":274,"weather":[{"id":800,"main":"Clear","description":"clear sky","icon":"01n"}]},{"dt":1586214000,"temp":284.12,"feels_like":281.57,"pressure":1027,"humidity":62,"dew_point":277.13,"clouds":2,"wind_speed":1.75,"wind_deg":276,"weather":[{"id":800,"main":"Clear","description":"clear sky","icon":"01n"}]},{"dt":1586217600,"temp":283.58,"feels_like":281.29,"pressure":1028,"humidity":65,"dew_point":277.37,"clouds":2,"wind_speed":1.43,"wind_deg":284,"weather":[{"id":800,"main":"Clear","description":"clear sky","icon":"01n"}]},{"dt":1586221200,"temp":283.09,"feels_like":280.97,"pressure":1028,"humidity":67,"dew_point":277.48,"clouds":0,"wind_speed":1.17,"wind_deg":303,"weather":[{"id":800,"main":"Clear","description":"clear sky","icon":"01n"}]},{"dt":1586224800,"temp":282.69,"feels_like":280.74,"pressure":1028,"humidity":70,"dew_point":277.58,"clouds":36,"wind_speed":1,"wind_deg":330,"weather":[{"id":802,"main":"Clouds","description":"scattered clouds","icon":"03n"}]},{"dt":1586228400,"temp":282.35,"feels_like":280.37,"pressure":1029,"humidity":72,"dew_point":277.67,"clouds":56,"wind_speed":1.06,"wind_deg":356,"weather":[{"id":803,"main":"Clouds","description":"broken clouds","icon":"04n"}]},{"dt":1586232000,"temp":281.97,"feels_like":279.74,"pressure":1029,"humidity":72,"dew_point":277.32,"clouds":66,"wind_speed":1.31,"wind_deg":23,"weather":[{"id":803,"main":"Clouds","description":"broken clouds","icon":"04n"}]},{"dt":1586235600,"temp":281.75,"feels_like":279.19,"pressure":1029,"humidity":69,"dew_point":276.56,"clouds":72,"wind_speed":1.57,"wind_deg":55,"weather":[{"id":803,"main":"Clouds","description":"broken clouds","icon":"04n"}]},{"dt":1586239200,"temp":281.68,"feels_like":278.94,"pressure":1030,"humidity":67,"dew_point":276,"clouds":70,"wind_speed":1.71,"wind_deg":68,"weather":[{"id":803,"main":"Clouds","description":"broken clouds","icon":"04d"}]},{"dt":1586242800,"temp":282.59,"feels_like":279.88,"pressure":1030,"humidity":65,"dew_point":276.51,"clouds":43,"wind_speed":1.78,"wind_deg":83,"weather":[{"id":802,"main":"Clouds","description":"scattered clouds","icon":"03d"}]},{"dt":1586246400,"temp":284.25,"feels_like":281.63,"pressure":1030,"humidity":63,"dew_point":277.54,"clouds":38,"wind_speed":1.94,"wind_deg":109,"weather":[{"id":802,"main":"Clouds","description":"scattered clouds","icon":"03d"}]},{"dt":1586250000,"temp":286.13,"feels_like":283.34,"pressure":1030,"humidity":57,"dew_point":278.1,"clouds":34,"wind_speed":2.28,"wind_deg":126,"weather":[{"id":802,"main":"Clouds","description":"scattered clouds","icon":"03d"}]},{"dt":1586253600,"temp":287.78,"feels_like":284.81,"pressure":1030,"humidity":51,"dew_point":278.06,"clouds":26,"wind_speed":2.53,"wind_deg":135,"weather":[{"id":802,"main":"Clouds","description":"scattered clouds","icon":"03d"}]},{"dt":1586257200,"temp":288.93,"feels_like":285.81,"pressure":1030,"humidity":46,"dew_point":277.56,"clouds":32,"wind_speed":2.62,"wind_deg":138,"weather":[{"id":802,"main":"Clouds","description":"scattered clouds","icon":"03d"}]},{"dt":1586260800,"temp":289.49,"feels_like":286.27,"pressure":1030,"humidity":42,"dew_point":276.69,"clouds":44,"wind_speed":2.56,"wind_deg":146,"weather":[{"id":802,"main":"Clouds","description":"scattered clouds","icon":"03d"}]},{"dt":1586264400,"temp":290.16,"feels_like":286.78,"pressure":1029,"humidity":38,"dew_point":275.92,"clouds":100,"wind_speed":2.58,"wind_deg":155,"weather":[{"id":804,"main":"Clouds","description":"overcast clouds","icon":"04d"}]},{"dt":1586268000,"temp":290.37,"feels_like":286.78,"pressure":1029,"humidity":38,"dew_point":275.98,"clouds":100,"wind_speed":2.92,"wind_deg":155,"weather":[{"id":804,"main":"Clouds","description":"overcast clouds","icon":"04d"}]},{"dt":1586271600,"temp":290.28,"feels_like":286.51,"pressure":1028,"humidity":38,"dew_point":276.08,"clouds":100,"wind_speed":3.17,"wind_deg":151,"weather":[{"id":804,"main":"Clouds","description":"overcast clouds","icon":"04d"}]},{"dt":1586275200,"temp":289.86,"feels_like":286.24,"pressure":1028,"humidity":40,"dew_point":276.5,"clouds":100,"wind_speed":3.03,"wind_deg":146,"weather":[{"id":804,"main":"Clouds","description":"overcast clouds","icon":"04d"}]},{"dt":1586278800,"temp":289.36,"feels_like":286.35,"pressure":1028,"humidity":45,"dew_point":277.51,"clouds":98,"wind_speed":2.48,"wind_deg":144,"weather":[{"id":804,"main":"Clouds","description":"overcast clouds","icon":"04d"}]},{"dt":1586282400,"temp":288.4,"feels_like":285.91,"pressure":1028,"humidity":51,"dew_point":278.6,"clouds":98,"wind_speed":2,"wind_deg":133,"weather":[{"id":804,"main":"Clouds","description":"overcast clouds","icon":"04d"}]},{"dt":1586286000,"temp":286.98,"feels_like":284.56,"pressure":1028,"humidity":57,"dew_point":278.8,"clouds":99,"wind_speed":1.98,"wind_deg":103,"weather":[{"id":804,"main":"Clouds","description":"overcast clouds","icon":"04n"}]},{"dt":1586289600,"temp":286.01,"feels_like":283.33,"pressure":1028,"humidity":60,"dew_point":278.69,"clouds":99,"wind_speed":2.3,"wind_deg":96,"weather":[{"id":804,"main":"Clouds","description":"overcast clouds","icon":"04n"}]},{"dt":1586293200,"temp":285.61,"feels_like":282.93,"pressure":1028,"humidity":61,"dew_point":278.45,"clouds":100,"wind_speed":2.26,"wind_deg":97,"weather":[{"id":804,"main":"Clouds","description":"overcast clouds","icon":"04n"}]},{"dt":1586296800,"temp":285.6,"feels_like":283.06,"pressure":1028,"humidity":61,"dew_point":278.41,"clouds":100,"wind_speed":2.06,"wind_deg":96,"weather":[{"id":804,"main":"Clouds","description":"overcast clouds","icon":"04n"}]},{"dt":1586300400,"temp":285.43,"feels_like":282.72,"pressure":1028,"humidity":61,"dew_point":278.22,"clouds":100,"wind_speed":2.26,"wind_deg":96,"weather":[{"id":804,"main":"Clouds","description":"overcast clouds","icon":"04n"}]},{"dt":1586304000,"temp":285.06,"feels_like":282.51,"pressure":1027,"humidity":62,"dew_point":278.17,"clouds":100,"wind_speed":1.99,"wind_deg":98,"weather":[{"id":804,"main":"Clouds","description":"overcast clouds","icon":"04n"}]},{"dt":1586307600,"temp":284.64,"feels_like":282.55,"pressure":1027,"humidity":65,"dew_point":278.34,"clouds":94,"wind_speed":1.42,"wind_deg":83,"weather":[{"id":804,"main":"Clouds","description":"overcast clouds","icon":"04n"}]},{"dt":1586311200,"temp":284.34,"feels_like":282.15,"pressure":1026,"humidity":66,"dew_point":278.43,"clouds":96,"wind_speed":1.55,"wind_deg":74,"weather":[{"id":804,"main":"Clouds","description":"overcast clouds","icon":"04n"}]},{"dt":1586314800,"temp":284.24,"feels_like":282.03,"pressure":1026,"humidity":67,"dew_point":278.59,"clouds":96,"wind_speed":1.6,"wind_deg":78,"weather":[{"id":804,"main":"Clouds","description":"overcast clouds","icon":"04n"}]},{"dt":1586318400,"temp":283.95,"feels_like":281.96,"pressure":1026,"humidity":69,"dew_point":278.71,"clouds":91,"wind_speed":1.34,"wind_deg":66,"weather":[{"id":804,"main":"Clouds","description":"overcast clouds","icon":"04n"}]},{"dt":1586322000,"temp":283.76,"feels_like":281.78,"pressure":1026,"humidity":71,"dew_point":278.83,"clouds":92,"wind_speed":1.39,"wind_deg":49,"weather":[{"id":804,"main":"Clouds","description":"overcast clouds","icon":"04n"}]},{"dt":1586325600,"temp":283.9,"feels_like":281.91,"pressure":1026,"humidity":72,"dew_point":279.1,"clouds":93,"wind_speed":1.5,"wind_deg":66,"weather":[{"id":804,"main":"Clouds","description":"overcast clouds","icon":"04d"}]},{"dt":1586329200,"temp":284.85,"feels_like":283.11,"pressure":1026,"humidity":69,"dew_point":279.48,"clouds":74,"wind_speed":1.24,"wind_deg":65,"weather":[{"id":803,"main":"Clouds","description":"broken clouds","icon":"04d"}]},{"dt":1586332800,"temp":286.52,"feels_like":284.75,"pressure":1025,"humidity":64,"dew_point":279.92,"clouds":73,"wind_speed":1.43,"wind_deg":62,"weather":[{"id":803,"main":"Clouds","description":"broken clouds","icon":"04d"}]},{"dt":1586336400,"temp":288.3,"feels_like":286.41,"pressure":1025,"humidity":59,"dew_point":280.6,"clouds":48,"wind_speed":1.76,"wind_deg":71,"weather":[{"id":802,"main":"Clouds","description":"scattered clouds","icon":"03d"}]},{"dt":1586340000,"temp":290.06,"feels_like":288.17,"pressure":1025,"humidity":55,"dew_point":281.26,"clouds":36,"wind_speed":1.97,"wind_deg":87,"weather":[{"id":802,"main":"Clouds","description":"scattered clouds","icon":"03d"}]},{"dt":1586343600,"temp":291.62,"feels_like":289.84,"pressure":1025,"humidity":52,"dew_point":281.75,"clouds":29,"wind_speed":2.03,"wind_deg":103,"weather":[{"id":802,"main":"Clouds","description":"scattered clouds","icon":"03d"}]},{"dt":1586347200,"temp":292.86,"feels_like":291.19,"pressure":1025,"humidity":48,"dew_point":281.75,"clouds":24,"wind_speed":1.86,"wind_deg":121,"weather":[{"id":801,"main":"Clouds","description":"few clouds","icon":"02d"}]},{"dt":1586350800,"temp":293.77,"feels_like":291.93,"pressure":1024,"humidity":44,"dew_point":281.44,"clouds":2,"wind_speed":1.94,"wind_deg":139,"weather":[{"id":800,"main":"Clear","description":"clear sky","icon":"01d"}]},{"dt":1586354400,"temp":294.29,"feels_like":292.47,"pressure":1024,"humidity":42,"dew_point":281.15,"clouds":1,"wind_speed":1.84,"wind_deg":158,"weather":[{"id":800,"main":"Clear","description":"clear sky","icon":"01d"}]},{"dt":1586358000,"temp":294.38,"feels_like":292.32,"pressure":1023,"humidity":42,"dew_point":281.14,"clouds":1,"wind_speed":2.21,"wind_deg":168,"weather":[{"id":800,"main":"Clear","description":"clear sky","icon":"01d"}]},{"dt":1586361600,"temp":293.91,"feels_like":291.65,"pressure":1023,"humidity":45,"dew_point":281.74,"clouds":4,"wind_speed":2.7,"wind_deg":163,"weather":[{"id":800,"main":"Clear","description":"clear sky","icon":"01d"}]},{"dt":1586365200,"temp":293.16,"feels_like":291.3,"pressure":1023,"humidity":50,"dew_point":282.51,"clouds":3,"wind_speed":2.44,"wind_deg":168,"weather":[{"id":800,"main":"Clear","description":"clear sky","icon":"01d"}]},{"dt":1586368800,"temp":291.86,"feels_like":290.07,"pressure":1023,"humidity":55,"dew_point":282.79,"clouds":2,"wind_speed":2.42,"wind_deg":169,"weather":[{"id":800,"main":"Clear","description":"clear sky","icon":"01d"}]}],"daily":[{"dt":1586174400,"sunrise":1586150592,"sunset":1586198470,"temp":{"day":285.09,"min":283.01,"max":285.09,"night":283.01,"eve":285.09,"morn":285.09},"feels_like":{"day":281.61,"night":280.69,"eve":281.61,"morn":281.61},"pressure":1024,"humidity":62,"dew_point":278.05,"wind_speed":3.34,"wind_deg":282,"weather":[{"id":800,"main":"Clear","description":"clear sky","icon":"01d"}],"clouds":6,"uvi":3.82},{"dt":1586260800,"sunrise":1586236857,"sunset":1586284970,"temp":{"day":289.49,"min":281.66,"max":290.28,"night":285.06,"eve":288.4,"morn":281.66},"feels_like":{"day":286.27,"night":282.51,"eve":285.91,"morn":278.91},"pressure":1030,"humidity":42,"dew_point":276.69,"wind_speed":2.56,"wind_deg":146,"weather":[{"id":802,"main":"Clouds","description":"scattered clouds","icon":"03d"}],"clouds":44,"uvi":4.14},{"dt":1586347200,"sunrise":1586323124,"sunset":1586371470,"temp":{"day":292.86,"min":283.9,"max":294.38,"night":287.16,"eve":291.86,"morn":283.9},"feels_like":{"day":291.19,"night":286.5,"eve":290.07,"morn":281.91},"pressure":1025,"humidity":48,"dew_point":281.75,"wind_speed":1.86,"wind_deg":121,"weather":[{"id":801,"main":"Clouds","description":"few clouds","icon":"02d"}],"clouds":24,"uvi":4.6},{"dt":1586433600,"sunrise":1586409391,"sunset":1586457970,"temp":{"day":292.61,"min":284.26,"max":292.61,"night":284.26,"eve":287.92,"morn":285.61},"feels_like":{"day":290.13,"night":281.37,"eve":284.78,"morn":284.48},"pressure":1023,"humidity":50,"dew_point":282.24,"wind_speed":3.15,"wind_deg":100,"weather":[{"id":500,"main":"Rain","description":"light rain","icon":"10d"}],"clouds":90,"rain":0.46,"uvi":4.92},{"dt":1586520000,"sunrise":1586495658,"sunset":1586544470,"temp":{"day":286.47,"min":284.37,"max":287.89,"night":286.25,"eve":287.36,"morn":284.37},"feels_like":{"day":286.24,"night":285.64,"eve":286.84,"morn":283.32},"pressure":1019,"humidity":82,"dew_point":283.57,"wind_speed":0.52,"wind_deg":99,"weather":[{"id":501,"main":"Rain","description":"moderate rain","icon":"10d"}],"clouds":100,"rain":6.62,"uvi":4.74},{"dt":1586606400,"sunrise":1586581926,"sunset":1586630970,"temp":{"day":286.54,"min":284.46,"max":289.65,"night":284.46,"eve":287.07,"morn":285.62},"feels_like":{"day":282.56,"night":281.06,"eve":283.08,"morn":283.83},"pressure":1016,"humidity":69,"dew_point":281.07,"wind_speed":4.96,"wind_deg":314,"weather":[{"id":501,"main":"Rain","description":"moderate rain","icon":"10d"}],"clouds":88,"rain":4.89,"uvi":4.19},{"dt":1586692800,"sunrise":1586668195,"sunset":1586717470,"temp":{"day":287.17,"min":282.81,"max":288.68,"night":284.43,"eve":287.84,"morn":282.81},"feels_like":{"day":284.14,"night":282.41,"eve":286.47,"morn":279.04},"pressure":1026,"humidity":62,"dew_point":280.05,"wind_speed":3.28,"wind_deg":351,"weather":[{"id":804,"main":"Clouds","description":"overcast clouds","icon":"04d"}],"clouds":96,"uvi":4.04},{"dt":1586779200,"sunrise":1586754465,"sunset":1586803970,"temp":{"day":291.41,"min":282.57,"max":293.86,"night":287.24,"eve":291.56,"morn":282.57},"feels_like":{"day":288.24,"night":285.84,"eve":289.52,"morn":279.19},"pressure":1028,"humidity":45,"dew_point":279.39,"wind_speed":3.26,"wind_deg":269,"weather":[{"id":804,"main":"Clouds","description":"overcast clouds","icon":"04d"}],"clouds":93,"uvi":3.88}]}
    response = {"a": "1", "b": "2"}
    return response


# Scheduing fetching
scheduler = orch.BackgroundScheduler(3, fetch_and_send)


# Running server
if __name__ == '__main__':
    app.run(host="localhost", port=member.port)
