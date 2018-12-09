import sys, simulator, requests, simulator, time, json, botActions

def getSim():
    url = 'http://127.0.0.1:5000/simulator/state'
    try:
        r = requests.get(url)
        if(r.status_code==200):
            sim = simulator.Simulator(fromDict=r.json())
            return sim
    except:
        pass
    return None

def sendBotAction(action):
    sim = getSim()
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

def sendStay():
    sendBotAction(simulator.Action.Stay)

def sendMoveUp():
    sendBotAction(simulator.Action.MoveUp)

def sendMoveDown():
    sendBotAction(simulator.Action.MoveDown)

def sendMoveLeft():
    sendBotAction(simulator.Action.MoveLeft)

def sendMoveRight():
    sendBotAction(simulator.Action.MoveRight)

def sendNextGame():
    sim = getSim()
    if(sim is not None):
        url = 'http://127.0.0.1:5000/simulator/new'
        print('posting to ' + url)
        try:
            r = requests.post(url)
        except Exception as e:
            pass