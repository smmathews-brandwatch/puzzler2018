import random
from flask import Flask, jsonify
from flask.json import JSONEncoder
from calendar import timegm
import time


class GameObject(object):
    def __init__(self):
        super(GameObject, self).__init__()

# A customized JSON encoder that knows about your SiteConfig class
class CustomJSONEncoder(JSONEncoder):
    def default(self, obj):
        if isinstance(obj, GameObject):
            return obj.__dict__
        return JSONEncoder.default(self, obj)

class Position(GameObject):
    def __init__(self):
        super(Position, self).__init__()

class Board(GameObject):
    def __init__(self, height, width):
        super(Board, self).__init__()
        self.height = height
        self.width = width

class Simulator(GameObject):
    def __init__(self, seed=None, height=640, width=640):
        super(Simulator, self).__init__()
        if(seed == None):
            seed = int(round(time.time() * 1000 * 1000))
        self.randomSeed = seed
        random.seed(seed)
        self.board = Board(height, width)