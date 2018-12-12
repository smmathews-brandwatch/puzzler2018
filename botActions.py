import sys, simulator, requests, simulator, time, json, botActions, server

class NetworkBot:
    def getScores(self):
        url = 'http://127.0.0.1:5000/roundScores'
        try:
            r = requests.get(url)
            if(r.status_code==200):
                scores = []
                for score in r.json():
                    scores.append(simulator.Score(fromDict=score))
                return scores
        except Exception as e:
            print(e)
        return None

    def getSim(self):
        url = 'http://127.0.0.1:5000/simulator/state'
        try:
            r = requests.get(url)
            if(r.status_code==200):
                if(simulator.ALL_ROUNDS_DONE == r.text):
                    return simulator.ALL_ROUNDS_DONE
                sim = simulator.Simulator(fromDict=r.json())
                return sim
        except Exception as e:
            print(e)
        return None

    def sendBotAction(self, action):
        sim = self.getSim()
        if(sim is not None):
            entityIdsToAction = []
            for entity in sim.board.entities:
                if entity.boardPiece == simulator.BoardPiece.Bot:
                    entityIdsToAction.append(simulator.EntityAction(id=entity.id,action=action))
            url = 'http://127.0.0.1:5000/simulator/tick'
            jsonData = server.CustomJSONEncoder().encode(simulator.TickRequest(entityIdsToAction=entityIdsToAction))
            print('posting to ' + url + ' json: ' + str(jsonData))
            try:
                r = requests.post(url, json=jsonData)
                print('received back: ' + str(r.json()))
            except Exception as e:
                print(e)

    def sendStay(self):
        self.sendBotAction(simulator.Action.Stay)

    def sendMoveUp(self):
        self.sendBotAction(simulator.Action.MoveUp)

    def sendMoveDown(self):
        self.sendBotAction(simulator.Action.MoveDown)

    def sendMoveLeft(self):
        self.sendBotAction(simulator.Action.MoveLeft)

    def sendMoveRight(self):
        self.sendBotAction(simulator.Action.MoveRight)

    def sendEndAllRounds(self):
        sim = self.getSim()
        if(sim is not None):
            url = 'http://127.0.0.1:5000/endAllRounds'
            print('posting to ' + url)
            try:
                r = requests.post(url)
            except Exception as e:
                print(e)

    def sendNextGame(self):
        sim = self.getSim()
        if(sim is not None):
            url = 'http://127.0.0.1:5000/simulator/new'
            print('posting to ' + url)
            try:
                r = requests.post(url)
            except Exception as e:
                print(e)

class SimulatorBot:
    def __init__(self, sim, entityIdsToAction, id):
        self.sim = sim
        self.entityIdsToAction = entityIdsToAction
        self.id = id

    def sendBotAction(self,action):
        self.entityIdsToAction.append(simulator.EntityAction(id=self.id, action=action))

    def sendStay(self):
        self.sendBotAction(simulator.Action.Stay)

    def sendMoveUp(self):
        self.sendBotAction(simulator.Action.MoveUp)

    def sendMoveDown(self):
        self.sendBotAction(simulator.Action.MoveDown)

    def sendMoveLeft(self):
        self.sendBotAction(simulator.Action.MoveLeft)

    def sendMoveRight(self):
        self.sendBotAction(simulator.Action.MoveRight)