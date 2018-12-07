import random
from flask import Flask, jsonify
from flask.json import JSONEncoder
from calendar import timegm
import time
from enum import Enum

class GameObject(object):
    def __init__(self):
        super().__init__()

class BoardPiece(GameObject):
    Empty = 1
    Bot = 2
    Enemy = 3
    Diamond = 4
    HomeBase = 5
    EnemyBase = 6

# A customized JSON encoder that knows about your SiteConfig class
class CustomJSONEncoder(JSONEncoder):
    item_separator = ','
    key_separator = ':'
    def default(self, obj):
        if isinstance(obj, GameObject):
            return obj.__dict__
        try:
            iterable = iter(o)
        except TypeError:
            pass
        else:
            return list(iterable)
        return JSONEncoder.default(self, obj)

class Position(GameObject):
    def __init__(self, x, y):
        super(Position, self).__init__()
        self.x = x
        self.y = y

class Entity(GameObject):
    def __init__(self, position, id, boardPiece):
        super(Entity, self).__init__()
        self.position = position
        self.id = id
        self.boardPiece = boardPiece

class Board(GameObject):
    def __init__(self, height, width, numEnemies):
        super().__init__()
        self.height = height
        self.width = width
        self.numEnemies = numEnemies
        self.initEntities()
    
    def initEntities(self):
        field = []
        field.append(BoardPiece.HomeBase)
        field.append(BoardPiece.EnemyBase)
        field.append(BoardPiece.Bot)
        for _i in range(self.numEnemies):
            field.append(BoardPiece.Enemy)
        while(len(field) < self.height*self.width):
            field.append(BoardPiece.Empty)
        random.shuffle(field)
        self.entities = []
        id = 0
        for x in range(self.width):
            for y in range(self.height):
                fieldPiece = field[y*self.width+x]
                if(fieldPiece > BoardPiece.Empty):
                    self.entities.append(Entity(Position(x,y),id,fieldPiece))
                    id += 1



class Score(GameObject):
    def __init__(self):
        super().__init__()
        # how many times did the bot return a diamond to your base
        self.rescued = 0
        # how many times did the enemy return a diamond to their base, or leave a diamond on the field at the end
        self.lost = 0

class Simulator(GameObject):
    def __init__(self, seed=None, height=640, width=640, numEnemies=1):
        super().__init__()
        if(seed == None):
            seed = int(round(time.time() * 1000 * 1000))
        self.randomSeed = seed
        random.seed(seed)
        self.board = Board(height, width, numEnemies)
