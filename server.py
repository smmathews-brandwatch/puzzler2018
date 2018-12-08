from flask import Flask,jsonify,url_for
import webbrowser
import simulator as sim
import json

app = Flask(__name__, static_folder=None)
app.env = 'development'
app.json_encoder = sim.CustomJSONEncoder
simulator = sim.Simulator()

@app.route('/', methods=['GET'])
def health():
    return 'Your server is running'

@app.route('/simulator/new', methods=['POST'])
def new():
    global simulator
    simulator = sim.Simulator(simRound=simulator.simRound+1)
    return jsonify(simulator)

@app.route('/simulator/state', methods=['GET'])
def state():
    global simulator
    return jsonify(simulator)

@app.cli.command()
def routes():
    'Display registered routes'
    rules = []
    for rule in app.url_map.iter_rules():
        methods = ','.join(sorted(rule.methods))
        rules.append((rule.endpoint, methods, str(rule)))

    sort_by_rule = operator.itemgetter(2)
    for endpoint, methods, rule in sorted(rules, key=sort_by_rule):
        route = '{:50s} {:25s} {}'.format(endpoint, methods, rule)
        print(route)

if __name__ == "__main__":
    webbrowser.open('http://127.0.0.1:5000/')
    app.run()
