import sys, simulator, requests, simulator, time, json, botActions

class NetworkBot:
    def getSim(self):
        url = 'http://127.0.0.1:5000/simulator/state'
        try:
            r = requests.get(url)
            if(r.status_code==200):
                sim = simulator.Simulator(fromDict=r.json())
                return sim
        except:
            pass
        return None

    def sendBotAction(self, action):
        sim = self.getSim()
        if(sim is not None):
            entityIdsToAction = []
            for entity in sim.board.entities:
                if entity.boardPiece == simulator.BoardPiece.Bot:
                    entityIdsToAction.append(simulator.EntityAction(id=entity.id,action=action))
            url = 'http://127.0.0.1:5000/simulator/tick'
            jsonData = simulator.CustomJSONEncoder().encode(simulator.TickRequest(entityIdsToAction=entityIdsToAction))
            print('posting to ' + url + ' json: ' + str(jsonData))
            try:
                r = requests.post(url, json=jsonData)
                print('received back: ' + str(r.json()))
            except Exception as e:
                print(e)
                pass

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

    def sendNextGame(self):
        sim = self.getSim()
        if(sim is not None):
            url = 'http://127.0.0.1:5000/simulator/new'
            print('posting to ' + url)
            try:
                r = requests.post(url)
            except Exception as e:
                pass

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