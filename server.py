from flask import Flask, jsonify, url_for, request
import webbrowser
from simulator import *
import json
import logging

app = Flask(__name__, static_folder=None)
app.env = 'development'
app.json_encoder = CustomJSONEncoder
simulator = Simulator()

log = logging.getLogger('werkzeug')
log.setLevel(logging.ERROR)

@app.route('/', methods=['GET'])
def health():
    return 'Your server is running'

curRounds = 0
maxRounds = 100

# Start a new simulation, results of the current simulation will be treated as final
@app.route('/simulator/new', methods=['POST'])
def new():
    global simulator
    roundScores.append(simulator.score)
    if(len(roundScores) < maxRounds):
        simulator = Simulator(simRound=simulator.simRound+1)
        return jsonify(simulator)
    return ALL_ROUNDS_DONE

roundScores = []

@app.route('/simulator/tick', methods=['POST'])
def tick():
    if(len(roundScores) >= maxRounds):
        return ALL_ROUNDS_DONE
    botsTick = TickRequest(fromDict=json.loads(request.get_json()))
    result = simulator.handleTickRequest(botsTick)
    response = jsonify(result)
    if(isinstance(result,BadTick)):
        response.status_code = 400
    if(simulator.frame >= simulator.maxFrames):
        new()
    return response

@app.route('/roundScores', methods=['GET'])
def scores():
    return jsonify(roundScores)

@app.route('/endAllRounds', methods=['POST'])
def endAllRounds():
    global maxRounds
    maxRounds = len(roundScores)

@app.route('/simulator/state', methods=['GET'])
def state():
    if(len(roundScores) >= maxRounds):
        return ALL_ROUNDS_DONE
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
    app.run()
