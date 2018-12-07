from flask import Flask,jsonify
import webbrowser
import simulator as sim
import json

app = Flask(__name__)
app.debug = True
app.env = 'development'
app.json_encoder = sim.CustomJSONEncoder
simulator = sim.Simulator()

@app.route('/', methods=['GET'])
def health():
    return 'Your server is running'

@app.route('/game/new', methods=['POST'])
def new():
    global simulator
    simulator = sim.Simulator()
    resp = jsonify(success=True)
    return resp

@app.route('/game/state', methods=['GET'])
def state():
    global simulator
    return jsonify(simulator)

if __name__ == "__main__":
    webbrowser.open('http://127.0.0.1:5000/')
    app.run()
