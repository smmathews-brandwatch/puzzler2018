import botActions
from collections import deque, namedtuple, defaultdict
import operator as op
from functools import reduce


forbiddenPathCost=1000
normalPathCost=8
encouragedPathCost=0
discouragedPathCost=25
name2Id={"bot":0,"bot_base":1,"collectibles":range(2,12), "enemy1":12,"enemy2":13, "enemy_base":14}
prevBoardData=None

inf = float('inf')
Edge = namedtuple('Edge', 'start, end, cost')

def ncr(n, r):
    r = min(r, n-r)
    numer = reduce(op.mul, range(n, n-r, -1), 1)
    denom = reduce(op.mul, range(1, r+1), 1)
    return numer / denom

def make_edge(start, end, cost=1):
  return Edge(start, end, cost)

class Graph:
    def __init__(self, edges):
        wrong_edges = [i for i in edges if len(i) not in [2, 3]]
        if wrong_edges:
            raise ValueError('Wrong edges data: {}'.format(wrong_edges))

        self.edges = [make_edge(*edge) for edge in edges]

    @property
    def vertices(self):
        return set(
            sum(
                ([edge.start, edge.end] for edge in self.edges), []
            )
        )

    def get_node_pairs(self, n1, n2, both_ends=True):
        if both_ends:
            node_pairs = [[n1, n2], [n2, n1]]
        else:
            node_pairs = [[n1, n2]]
        return node_pairs

    def remove_edge(self, n1, n2, both_ends=True):
        node_pairs = self.get_node_pairs(n1, n2, both_ends)
        edges = self.edges[:]
        for edge in edges:
            if [edge.start, edge.end] in node_pairs:
                self.edges.remove(edge)
    def add_edge(self, n1, n2, cost=1, both_ends=True):
        node_pairs = self.get_node_pairs(n1, n2, both_ends)
        for edge in self.edges:
            if [edge.start, edge.end] in node_pairs:
                return ValueError('Edge {} {} already exists'.format(n1, n2))
        self.edges.append(Edge(start=n1, end=n2, cost=cost))
        if both_ends:
            self.edges.append(Edge(start=n2, end=n1, cost=cost))

    @property
    def neighbours(self):
        neighbours = {vertex: set() for vertex in self.vertices}
        for edge in self.edges:
            neighbours[edge.start].add((edge.end, edge.cost))
        return neighbours

    def dijkstra(self, source, dest):
        assert source in self.vertices, 'Such source node doesn\'t exist'
        distances = {vertex: inf for vertex in self.vertices}
        previous_vertices = {
            vertex: None for vertex in self.vertices
        }
        distances[source] = 0
        vertices = self.vertices.copy()
        while vertices:
            current_vertex = min(
                vertices, key=lambda vertex: distances[vertex])
            vertices.remove(current_vertex)
            if distances[current_vertex] == inf:
                break
            for neighbour, cost in self.neighbours[current_vertex]:
                alternative_route = distances[current_vertex] + cost
                if alternative_route < distances[neighbour]:
                    distances[neighbour] = alternative_route
                    previous_vertices[neighbour] = current_vertex
        path, current_vertex = deque(), dest
        while previous_vertices[current_vertex] is not None:
            path.appendleft(current_vertex)
            current_vertex = previous_vertices[current_vertex]
        if path:
            path.appendleft(current_vertex)
        return path

def getManhattanDistance(c1, c2): return abs(c1[0] - c2[0]) + abs(c1[1] - c2[1])

def getBoardData(sim, prevBoardData):
    boardData={}
    board = sim.board
    boardData["withBot"]= 0
    boardData["freeIds"]= []
    boardData["withEnemy1"]=  0
    boardData["withEnemy2"] = 0
    boardData["enemyCapturedIds"]=[]
    boardData['frame']=sim.frame
    for entity in board.entities:
        boardData[entity.id] = (entity.position.x, entity.position.y)
        if entity.boardPiece == "collectible" and entity.ownerId is None:
            boardData["freeIds"].append(entity.id)
        elif entity.boardPiece == "collectible" and entity.ownerId == name2Id["enemy1"]:
            boardData["withEnemy1"]+=1
            boardData["enemyCapturedIds"].append(entity.id)
        elif entity.boardPiece == "collectible" and entity.ownerId == name2Id["enemy2"]:
            boardData["withEnemy2"]+=1
            boardData["enemyCapturedIds"].append(entity.id)
        elif entity.boardPiece == "collectible" and entity.ownerId == name2Id["bot"]:
            boardData["withBot"]+=1
    if prevBoardData is not None:
        if boardData['withBot'] - prevBoardData['withBot'] < 0:
            boardData['justVisitedBotBase'] = True
        else:
            boardData['justVisitedBotBase'] = False
    else:
            boardData['justVisitedBotBase'] = False

    return boardData

def getNeighbors(edge):
    neighbors = []
    if edge[0] - 1 >= 0: neighbors.append((edge[0] - 1, edge[1]))
    if edge[0] + 1 < 10: neighbors.append((edge[0] + 1, edge[1]))
    if edge[1] - 1 >= 0: neighbors.append((edge[0], edge[1] - 1))
    if edge[1] + 1 < 10: neighbors.append((edge[0], edge[1] + 1))
    return neighbors

def getDefaultGraphDict(boardData,n = 10):
    graphDict = {}
    for i in range(n):
        for j in range(n):
            node = (i, j)
            neighbors = getNeighbors(node)
            for neighbor in neighbors:
                if neighbor==boardData[name2Id["enemy_base"]]:
                    graphDict[(node, neighbor)] = (node, neighbor, 1000)
                else:
                    graphDict[(node,neighbor)]=(node, neighbor, 1)
    return graphDict

def doNotTouchCollectibles(boardData):
    if boardData["withBot"] == 5: return True
    return False

def doNotTouchBase(boardData):
    if boardData['justVisitedBotBase'] or boardData["withBot"]==0 or \
            (len(boardData["freeIds"])+boardData["withBot"] <= 5 and boardData['frame']<85):
        return True
    return False

def updateNeighborhood(graphDict, node, value):
    neighbors = getNeighbors(node)
    for neighbor in neighbors:
        graphDict[(neighbor, node)] = (neighbor, node, value)

def updateGraphDict(graphDict, boardData):
    if doNotTouchBase(boardData):
        updateNeighborhood(graphDict, boardData[name2Id["bot_base"]], forbiddenPathCost)
    else:
        updateNeighborhood(graphDict, boardData[name2Id["bot_base"]], encouragedPathCost)
    if doNotTouchCollectibles(boardData):
        for collectible in boardData["freeIds"]: updateNeighborhood(graphDict, boardData[collectible], forbiddenPathCost)
    else:
        for collectible in boardData["freeIds"]: updateNeighborhood(graphDict, boardData[collectible], encouragedPathCost)

    updateNeighborhood(graphDict, boardData[name2Id["enemy1"]], discouragedPathCost)
    updateNeighborhood(graphDict, boardData[name2Id["enemy2"]], discouragedPathCost)

def gotoBase(boardData):
    if (canLikelyGoToBaseInTime(boardData) and  (boardData["withBot"] == 5 or (len(boardData["freeIds"]) == 0 and boardData["withBot"] > 0))) \
       or (boardData['frame'] > 75 and boardData['withBot']>0 and
           (100 - boardData['frame']) - getManhattanDistance(boardData[name2Id["bot"]],boardData[name2Id["bot_base"]]) <=3) :
        return True
    return False

def getNumberOfPathsInGrid(start, end):
    x1 = abs(start[0]-end[0])
    x2 = abs(start[1] - end[1])
    n = x1+x2
    return ncr(n,x1)

def getCollectibleAtHighestRisk(boardData):
    riskProfile = {}
    for collectible in boardData["freeIds"]:
        collectibleLocation = boardData[collectible]
        distb = getManhattanDistance(boardData[name2Id["bot"]], collectibleLocation)
        distNode2base = getManhattanDistance(boardData[name2Id["bot_base"]], collectibleLocation)
        if distb+distNode2base >= 100-boardData['frame']:
            continue
        dist1 = getManhattanDistance(boardData[name2Id["enemy1"]], collectibleLocation)
        dist2 = getManhattanDistance(boardData[name2Id["enemy2"]], collectibleLocation)
        p1 = getNumberOfPathsInGrid(boardData[name2Id["enemy1"]], collectibleLocation)*(0.25**dist1)
        p2 = getNumberOfPathsInGrid(boardData[name2Id["enemy2"]], collectibleLocation)*(0.25**dist2)
        riskProfile[collectible] = ((p1+p2)*(1/distb))**0.5
    if len(riskProfile)>0:
        riskProfile = sorted(riskProfile, key=riskProfile.get, reverse=True)
        return riskProfile[0]
    return None

def getBestLocationForObstruction(boardData):
    dist1 = getManhattanDistance(boardData[name2Id["enemy_base"]], boardData[name2Id["enemy1"]])
    dist2 = getManhattanDistance(boardData[name2Id["enemy_base"]], boardData[name2Id["enemy2"]])
    enemy1Carry = boardData["withEnemy1"]
    enemy2Carry = boardData["withEnemy2"]
    if enemy1Carry == 0 and enemy2Carry == 0:
        return None
    elif enemy2Carry == 0:
        enemyTargetLocation = boardData[name2Id["enemy1"]]
    elif enemy1Carry == 0:
        enemyTargetLocation = boardData[name2Id["enemy2"]]
    elif dist1 / enemy1Carry < dist2 / enemy2Carry:
        enemyTargetLocation = boardData[name2Id["enemy1"]]
    else:
        enemyTargetLocation = boardData[name2Id["enemy2"]]
    return ((enemyTargetLocation[0] + boardData[name2Id["enemy_base"]][0]) // 2,
              (enemyTargetLocation[1] + boardData[name2Id["enemy_base"]][1]) // 2)

def getPathAction(boardData, graphDict, node1Loc, node2Loc):
    updateGraphDict(graphDict, boardData)
    graph = Graph(list(graphDict.values()))
    path = list(graph.dijkstra(node1Loc, node2Loc))
    actionPath= turnActionListIntoActions(path[0:2])
    if len(actionPath)>0:
        return actionPath[0]
    else:
        return 'stay'

def canLikelyGoToBaseInTime(boardData):
    if getManhattanDistance(boardData[name2Id['bot']],boardData[name2Id['bot_base']])-(100-boardData['frame'])>=0:
        return False
    return True

def pathToBaseIsObstructed(boardData):
    graphDict = getDefaultGraphDict(boardData)
    for collectible in boardData["freeIds"]:
        updateNeighborhood(graphDict, boardData[collectible], forbiddenPathCost)
    graph = Graph(list(graphDict.values()))
    path = list(graph.dijkstra(boardData[name2Id["bot"]], boardData[name2Id["bot_base"]]))
    cost = 0
    for i in range(len(path)-1):
        cost += graphDict[(path[i],path[i+1])][2]

    if cost >= forbiddenPathCost:
        return True
    else:
        return False

def turnActionListIntoActions(actionList):
    actionL = []
    for i in range(len(actionList)-1):
        delta = actionList[i+1][0]*10+actionList[i+1][1]-actionList[i][0]*10-actionList[i][1]
        if delta==10:
            actionL.append('right')
        elif delta==-10:
            actionL.append('left')
        elif delta == -1:
            actionL.append('up')
        elif delta == 1:
            actionL.append('down')
    return actionL

def earlyExit(boardData):
    withBot= boardData["withBot"]
    withE1 = boardData["withEnemy1"]
    withE2 = boardData["withEnemy1"]
    bDist = getManhattanDistance(boardData[name2Id["enemy1"]],boardData[name2Id["bot_base"]])
    e1Dist = getManhattanDistance(boardData[name2Id["enemy1"]],boardData[name2Id["enemy_base"]])
    e2Dist = getManhattanDistance(boardData[name2Id["enemy2"]], boardData[name2Id["enemy_base"]])
    expectedEScore = withE1*(0.25**e1Dist)+withE2*(0.25**e2Dist)
    expectedBScore = withBot*(0.95**bDist)
    if withE1+withE2 == 3 and expectedEScore>expectedBScore:
        return True
    return False

def getAction(sim, riskFunction=getCollectibleAtHighestRisk):
    global prevBoardData
    boardData = getBoardData(sim, prevBoardData)
    if earlyExit(boardData): return 'next'
    prevBoardData = boardData
    graphDict = getDefaultGraphDict(boardData)
    if gotoBase(boardData) or pathToBaseIsObstructed(boardData):
        return getPathAction(boardData, graphDict, boardData[name2Id["bot"]], boardData[name2Id["bot_base"]])
    nextId = riskFunction(boardData)
    print(nextId)
    if nextId is not None:
        nextLoc = boardData[nextId]
        return getPathAction(boardData, graphDict, boardData[name2Id["bot"]], nextLoc)
    else:
        return 'next'

class YourBot:
    def doAction(self, botActionsWrapper):
        sim = botActionsWrapper.getSim()
        if not sim == "all rounds done":
            action = getAction(sim)
            if action=='left': botActionsWrapper.sendMoveLeft()
            elif action=='right': botActionsWrapper.sendMoveRight()
            elif action == 'up': botActionsWrapper.sendMoveUp()
            elif action == 'down': botActionsWrapper.sendMoveDown()
            elif action=='stay':botActionsWrapper.sendStay()
            elif action=='next': botActionsWrapper.sendNextGame()
            else: botActionsWrapper.sendNextGame()
            return True
        else:
            return False

if __name__ == "__main__":
    bot = YourBot()
    while(1):
        if not bot.doAction(botActions.NetworkBot()):
            break
