import random
from flask import Flask, jsonify
from flask.json import JSONEncoder
from calendar import timegm
import time
from enum import Enum
import baseBot, botActions

ALL_ROUNDS_DONE = "all rounds done"
ALLOW_STEALING = False

class GameObject(object):
    def __init__(self):
        super().__init__()
    def __init__(self, **entries):
        self.__dict__.update(entries)

class Action(GameObject):
    Stay = 'stay'
    MoveUp = 'up'
    MoveDown = 'down'
    MoveLeft = 'left'
    MoveRight = 'right'

class EntityAction(GameObject):
    def __init__(self, fromDict=None, id=None, action=None):
        super().__init__()
        if(fromDict == None):
            self.id = id
            self.action = action
        else:
            self.id = fromDict['id']
            self.action = fromDict['action']

class TickBase(GameObject):
    def __init__(self, fromDict=None, entityIdsToAction=None):
        super().__init__()
        if(fromDict == None):
            self.entityIdsToAction = entityIdsToAction if entityIdsToAction is not None else []
        else:
            self.entityIdsToAction = []
            if('entityIdsToAction' in fromDict):
                for entityIdToAction in fromDict['entityIdsToAction']:
                    self.entityIdsToAction.append(EntityAction(fromDict=entityIdToAction))

class BoardPiece(GameObject):
    Empty = 'empty'
    Bot = 'bot'
    Enemy = 'enemy'
    Collectible = 'collectible'
    BotBase = 'bot_base'
    EnemyBase = 'enemy_base'

class Position(GameObject):
    def __init__(self, fromDict=None, x=None, y=None):
        super(Position, self).__init__()
        if(fromDict == None):
            self.x = x
            self.y = y
        else:
            self.x = fromDict['x']
            self.y = fromDict['y']
    
    def __eq__(self, other):
        if isinstance(other, Position):
            return self.x == other.x and self.y == other.y
        return NotImplemented

class Entity(GameObject):
    def __init__(self, fromDict=None, position=None, id=None, boardPiece=None, ownerId=None):
        super(Entity, self).__init__()
        if(fromDict == None):
            self.position = position
            self.id = id
            self.boardPiece = boardPiece
            self.ownerId = ownerId
        else:
            self.position = Position(fromDict=fromDict['position'])
            self.id = fromDict['id']
            self.boardPiece = fromDict['boardPiece']
            self.ownerId = fromDict['ownerId']
        
    def __eq__(self, other):
        if isinstance(other, Entity):
            return self.id == other.id and self.id == other.id
        return NotImplemented

class Board(GameObject):
    def __init__(self, fromDict=None, height=None, width=None, numEnemies=None, numCollectibles=None):
        super().__init__()
        if(fromDict == None):
            self.height = height
            self.width = width
            self.numEnemies = numEnemies
            self.numCollectibles = numCollectibles
            self.initEntities()
        else:
            self.height = fromDict['height']
            self.width = fromDict['width']
            self.numEnemies = fromDict['numEnemies']
            self.numCollectibles = fromDict['numCollectibles']
            self.entities = []
            for entity in fromDict['entities']:
                self.entities.append(Entity(fromDict=entity))
    
    def sortEntitiesByPieceKey(self,entity):
        return entity.boardPiece

    def initEntities(self):
        field = []
        field.append(BoardPiece.BotBase)
        field.append(BoardPiece.EnemyBase)
        field.append(BoardPiece.Bot)
        for _i in range(self.numEnemies):
            field.append(BoardPiece.Enemy)
        for _i in range(self.numCollectibles):
            field.append(BoardPiece.Collectible)
        while(len(field) < self.height*self.width):
            field.append(BoardPiece.Empty)
        random.shuffle(field)
        self.entities = []
        for x in range(self.width):
            for y in range(self.height):
                boardPiece = field[y*self.width+x]
                if(boardPiece != BoardPiece.Empty):
                    self.entities.append(Entity(position=Position(x=x,y=y),boardPiece=boardPiece))
        sortedEntities = sorted(self.entities, key=self.sortEntitiesByPieceKey)
        id = 0
        for entity in sortedEntities:
            entity.id = id
            id += 1

    def calculateScore(self):
        toReturn = Score()
        for entity in self.entities:
            if entity.boardPiece == BoardPiece.Collectible and entity.ownerId is not None:
                for otherEntity in self.entities:
                    if otherEntity.id == entity.ownerId:
                        if otherEntity.boardPiece == BoardPiece.EnemyBase:
                            toReturn.lost += 1
                        elif otherEntity.boardPiece == BoardPiece.BotBase:
                            toReturn.rescued += 1
                        break
        return toReturn

class Score(GameObject):
    def __init__(self, fromDict=None):
        super().__init__()
        if(fromDict is None):
            # how many times did the bot return a collectible to your base
            self.rescued = 0
            # how many times did the enemy return a collectible to their base
            self.lost = 0
        else:
            self.rescued = fromDict['rescued']
            self.lost = fromDict['lost']

EnemyBots = [baseBot.BaseBot()]

class Simulator(GameObject):
    def __init__(self, fromDict=None, seed=None, height=10, width=10, numEnemies=2, numCollectibles=10, simRound=0, maxFrames=100, maxCollectibles=5):
        super().__init__()
        if(fromDict == None):
            if(seed == None):
                seed = int(round(time.time() * 1000 * 1000))
            self.randomSeed = seed
            random.seed(seed)
            self.board = Board(height=height, width=width, numEnemies=numEnemies, numCollectibles=numCollectibles)
            self.frame = 0
            self.simRound = simRound
            self.score = self.board.calculateScore()
            self.maxFrames = maxFrames
            self.maxCollectibles = maxCollectibles
        else:
            self.randomSeed = fromDict['randomSeed']
            self.board = Board(fromDict=fromDict['board'])
            self.frame = fromDict['frame']
            self.simRound = fromDict['simRound']
            self.score = Score(fromDict=fromDict['score'])
            self.maxFrames = fromDict['maxFrames']
            self.maxCollectibles = fromDict['maxCollectibles']
    
    def transfer(self, oldEntity, newEntity):
        for otherEntity in self.board.entities:
            if otherEntity.ownerId == oldEntity.id:
                otherEntity.ownerId = newEntity.id

    def getNumCollectiblesEntityIsCarrying(self, entity):
        num = 0
        for otherEntity in self.board.entities:
            if(otherEntity.ownerId == entity.id):
                num += 1
        return num

    def moveEntity(self, entity, vector, entityIdToAction):
        entity.position.x += vector.x
        entity.position.y += vector.y
        # check if entity must stay because they'd go over the edge of the board
        if(entity.position.x > self.board.width-1 or entity.position.x < 0 or
            entity.position.y > self.board.height-1 or entity.position.y < 0):
            entityIdToAction.action = Action.Stay
            entity.position.x -= vector.x
            entity.position.y -= vector.y
        #check if the entity is colliding with another entity
        if(entity.boardPiece == BoardPiece.Bot or entity.boardPiece == BoardPiece.Enemy):
            for otherEntity in self.board.entities:
                if otherEntity.ownerId is None and otherEntity != entity and otherEntity.position == entity.position:
                    # check if the bot or enemy are now touching a base or collectible
                    if(otherEntity.boardPiece == BoardPiece.Collectible and self.getNumCollectiblesEntityIsCarrying(entity) < self.maxCollectibles):
                        #check if the bot or enemy already has the max number of collectibles
                        otherEntity.ownerId = entity.id
                    else:
                        entityIdToAction.action = Action.Stay
                        entity.position.x -= vector.x
                        entity.position.y -= vector.y
                        if(ALLOW_STEALING and otherEntity.boardPiece != entity.boardPiece and (otherEntity.boardPiece == BoardPiece.Bot or otherEntity.boardPiece == BoardPiece.Enemy)):
                            # steal the other entitie's collectibles
                            self.transfer(otherEntity,entity)
                        elif((otherEntity.boardPiece == BoardPiece.EnemyBase and entity.boardPiece == BoardPiece.Enemy) or
                            (otherEntity.boardPiece == BoardPiece.BotBase and entity.boardPiece == BoardPiece.Bot)):
                            #transfer any collectibles from this bot/enemy to base
                            self.transfer(entity,otherEntity)

    def tickAll(self, entityIdsToAction):
        for entityIdToAction in entityIdsToAction:
            for entity in self.board.entities:
                    if(entity.id == entityIdToAction.id):
                        if(entityIdToAction.action == Action.MoveUp):
                            self.moveEntity(entity, Position(x=0, y=-1), entityIdToAction)
                        elif(entityIdToAction.action == Action.MoveDown):
                            self.moveEntity(entity, Position(x=0, y=1), entityIdToAction)
                        elif(entityIdToAction.action == Action.MoveLeft):
                            self.moveEntity(entity, Position(x=-1, y=0), entityIdToAction)
                        elif(entityIdToAction.action == Action.MoveRight):
                            self.moveEntity(entity, Position(x=1, y=0), entityIdToAction)
                        break
        self.frame += 1
        self.score = self.board.calculateScore()

    def handleTickRequest(self, tickRequest):
        badIds = set()
        duplicateIds = set()
        seenIds = set()
        for entityIdToAction in tickRequest.entityIdsToAction:
            if entityIdToAction.id not in seenIds:
                seenIds.add(entityIdToAction.id)
                for entity in self.board.entities:
                    if(entity.id == entityIdToAction.id):
                        foundEntity = True
                        if(entity.boardPiece != BoardPiece.Bot):
                            badIds.add(entityIdToAction.id)
                            break
                if(not foundEntity):
                    badIds.add(entityIdToAction.id)
            else:
                duplicateIds.add(entityIdToAction.id)
        if(len(badIds) > 0 or len(duplicateIds) > 0):
            return BadTick(badIds=badIds, duplicateIds=duplicateIds)
        response = TickResponse()

        for entity in self.board.entities:
            if entity.boardPiece == BoardPiece.Enemy:
                enemyBotsActions = botActions.SimulatorBot(self, response.entityIdsToAction, entity.id)
                eb = EnemyBots[entity.id % len(EnemyBots)]
                eb.doAction(enemyBotsActions)
            elif entity.boardPiece == BoardPiece.Bot:
                for requestAction in tickRequest.entityIdsToAction:
                    if(requestAction.id == entity.id):
                        response.entityIdsToAction.append(requestAction)
                        break
        # TODO: figure out the enemies part of the tick
        self.tickAll(response.entityIdsToAction)
        return TickResponse(entityIdsToAction=response.entityIdsToAction)

class TickResponse(TickBase):
    def __init__(self, fromDict=None, entityIdsToAction=None):
        super().__init__(fromDict=fromDict, entityIdsToAction=entityIdsToAction)

class TickRequest(TickBase):
    def __init__(self, fromDict=None, entityIdsToAction=None):
        super().__init__(fromDict=fromDict, entityIdsToAction=entityIdsToAction)

class BadTick(GameObject):
    def __init__(self, fromDict=None, badIds=None, duplicateIds=None):
        super().__init__()
        if(fromDict == None):
            self.badIds = badIds
            self.duplicateIds = duplicateIds
        else:
            self.badIds = fromDict['badIds']
            self.duplicateIds = fromDict['duplicateIds']

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