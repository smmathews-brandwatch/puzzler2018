import botActions, time, random, queue, math
from simulator import BoardPiece, Action, Position, ALL_ROUNDS_DONE

# soup nazi bot (no collectibles for you!)
# 1) Attempt to deny the enemy bots their highest likelyhood collectibles right at the beginning
# 2) Assume the bots are just as likely to attempt to move up, down, left, or right every frame.
# 3) Based on bing, aykut, and damian's current sores (<9), don't worry too much about getting the 10th collectible.

def takeFirst(elem):
    return elem[0]

class Util:
    def __init__(self, sim):
        self.numCollectiblesOnPlayer = 0
        self.numCollectiblesLeft = 0
        self.numCollectiblesOnEnemies = 0
        self.playerId = None
        self.enemyIds = []
        self.enemyPositions = []
        self.playerPosition = None
        self.riskiestCollectibles = []
        risk = 100000
        for otherEntity in sim.board.entities:
            if otherEntity.boardPiece == BoardPiece.Bot:
                self.playerId = otherEntity.id
                self.playerPosition = otherEntity.position
            elif otherEntity.boardPiece == BoardPiece.Enemy:
                self.enemyIds.append(otherEntity.id)
                self.enemyPositions.append(otherEntity.position)
            elif otherEntity.boardPiece == BoardPiece.BotBase:
                self.botBasePosition = otherEntity.position
        for otherEntity in sim.board.entities:
            if otherEntity.boardPiece == BoardPiece.Collectible:
                if otherEntity.ownerId == self.playerId:
                    self.numCollectiblesOnPlayer += 1
                elif otherEntity.ownerId == None:
                    self.numCollectiblesLeft += 1
                    thisRisk = 1000
                    for enemyPos in self.enemyPositions:
                        thisRisk =  min(thisRisk,abs(enemyPos.x - otherEntity.position.x) + abs(enemyPos.y - otherEntity.position.y))
                    self.riskiestCollectibles.append((thisRisk,otherEntity.position))
                elif otherEntity.ownerId in self.enemyIds:
                    self.numCollectiblesOnEnemies += 1
        self.riskiestCollectibles.sort(key=takeFirst)

class Node:
    def __init__(self, position, g, h, parent, move, numCollectiblesOnPath, boardPiece):
        self.position = position
        self.g = g
        self.h = h
        self.f = g+h-(numCollectiblesOnPath*0.75)
        self.parent = parent
        self.move = move
        self.numCollectiblesOnPath = numCollectiblesOnPath
        self.boardPiece = boardPiece

    def __eq__(self, other):
        return self.position == other.position

# do an A* search to get from the start to the end
class Path:
    def __init__(self, sim, util, start, end):
        open_list = []
        closed_list = []
        field = []
        while len(field) < sim.board.height*sim.board.width:
            field.append(BoardPiece.Empty)
        for otherEntity in sim.board.entities:
            if otherEntity.ownerId is None:
                field[otherEntity.position.y*sim.board.width + otherEntity.position.x] = otherEntity.boardPiece
        
        start_node  = Node(start, 0, 0, None, None, 0, None)
        end_node = Node(end, 0, 0, None, None, 0, None)
        open_list.append(start_node)

        self.move = None
        self.collectibles = 0
        while len(open_list) > 0 and len(open_list) < 1000:
            # Get the current node
            current_node = open_list[0]
            current_index = 0
            for index, item in enumerate(open_list):
                if item.f < current_node.f:
                    current_node = item
                    current_index = index
            
            # Pop current off open list, add to closed list
            open_list.pop(current_index)
            closed_list.append(current_node)

            # Found the goal
            if current_node == end_node:
                current = current_node
                self.collectibles = current.numCollectiblesOnPath
                while current.move is not None:
                    self.move = current.move
                    current = current.parent
                return
            
            # generate the children
            children = []
            for moveTuple in [(Action.MoveUp,(0,-1)), (Action.MoveDown,(0,1)), (Action.MoveLeft,(-1,0)), (Action.MoveRight,(1,0))]:
                newPosition = Position(x=current_node.position.x+moveTuple[1][0], y=current_node.position.y+moveTuple[1][1])
                move = moveTuple[0]
                if(newPosition.x >= 0 and newPosition.x < sim.board.width and newPosition.y >= 0 and newPosition.y < sim.board.height):
                    piece = field[newPosition.y*sim.board.width + newPosition.x]
                    g = current_node.g + 1
                    h = ((newPosition.x - end_node.position.x) ** 2) + ((newPosition.y - end_node.position.y) ** 2)
                    numCollectiblesOnPath = current_node.numCollectiblesOnPath
                    if(piece == BoardPiece.Collectible and current_node.numCollectiblesOnPath < sim.maxCollectibles):
                        numCollectiblesOnPath += 1
                        children.append(Node(newPosition, g, h, current_node, move,numCollectiblesOnPath, piece))
                    elif(newPosition == end or piece == BoardPiece.Empty):
                        children.append(Node(newPosition, g, h, current_node, move, numCollectiblesOnPath, piece))

            # Loop through children
            for child in children:
                # Child is on the closed list
                for closed_child in closed_list:
                    if child == closed_child:
                        continue
                # Child is already in the open list
                for open_node in open_list:
                    if child == open_node and child.g > open_node.g:
                        continue

                # Add the child to the open list
                open_list.append(child)

class PathToPlayerBase(Path):
    def __init__(self, sim, util):
        start = None
        end = None
        super().__init__(sim, util, util.playerPosition, util.botBasePosition)

class PathToRiskiest(Path):
    def __init__(self, sim, util):
        start = None
        end = None
        super().__init__(sim, util, util.playerPosition, util.riskiestPosition)

class YourBot:
    def doAction(self, botActionsWrapper):
        sim = botActionsWrapper.getSim()
        if(sim != None and sim != ALL_ROUNDS_DONE):
            util = Util(sim)
            path = None
            if util.numCollectiblesOnPlayer > 0:
                print('nice')
                toBase = PathToPlayerBase(sim, util)
                # also check if there are barely enough frames to make it back
                if toBase.collectibles+util.numCollectiblesOnPlayer == sim.maxCollectibles or (util.numCollectiblesLeft > 0 and toBase.collectibles+util.numCollectiblesOnPlayer == util.numCollectiblesLeft):
                    path = toBase
            if util.riskiestCollectibles != None and path == None:
                i = 0
                while((path == None or path.move is None) and (i < len(util.riskiestCollectibles))):
                    print(str(i))
                    path = Path(sim, util, util.playerPosition, util.riskiestCollectibles[i][1])
                    i += 1

            if path != None:
                if path.move == Action.MoveUp:
                    actionsThisRound = botActionsWrapper.sendMoveUp()
                elif  path.move == Action.MoveDown:
                    actionsThisRound = botActionsWrapper.sendMoveDown()
                elif  path.move == Action.MoveLeft:
                    actionsThisRound = botActionsWrapper.sendMoveLeft()
                elif  path.move == Action.MoveRight:
                    actionsThisRound = botActionsWrapper.sendMoveRight()
            else:
                print('ending this game')
                botActionsWrapper.sendNextGame()

if __name__ == "__main__":
    bot = YourBot()
    while(1):
        bot.doAction(botActions.NetworkBot())