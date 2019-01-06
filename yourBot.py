import botActions, time, random, queue, math
from simulator import BoardPiece, Action, Position

# soup nazi bot (no collectibles for you!)
# 1) Attempt to deny the enemy bots their highest likelyhood collectibles right at the beginning
# 2) Assume the bots are just as likely to attempt to move up, down, left, or right every frame.
# 3) Based on bing, aykut, and damian's current sores (<9), don't worry too much about getting the 10th collectible.

class Util:
    def __init__(self, sim):
        self.numCollectiblesOnPlayer = 0
        self.numCollectiblesOnBotOneMoveFromBase = 0
        self.playerId = None
        self.enemyIds = []
        for otherEntity in sim.board.entities:
            if otherEntity.boardPiece == BoardPiece.Bot:
                self.playerId = otherEntity.id
            elif otherEntity.boardPiece == BoardPiece.Enemy:
                self.enemyIds.append(otherEntity.id)
        if otherEntity.ownerId == self.playerId:
            self.numCollectiblesOnPlayer += 1
        elif otherEntity.ownerId in self.enemyIds:
            self.enemyIds.append(otherEntity.ownerId)

class Node:
    def __init__(self, position, g, h, parent, move, numCollectiblesOnPath, boardPiece):
        self.position = position
        self.g = g
        self.h = h
        self.f = g+h-(numCollectiblesOnPath*1.25)
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

        while len(open_list) > 0:
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
                    if current.boardPiece == BoardPiece.Collectible:
                        self.collectibles += 1
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
                    h = math.sqrt(((newPosition.x - end_node.position.x) ** 2) + ((newPosition.y - end_node.position.y) ** 2))
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
        for otherEntity in sim.board.entities:
            if util.playerId == otherEntity.id:
                start = otherEntity.position
            elif otherEntity.boardPiece == BoardPiece.BotBase:
                end = otherEntity.position
        super().__init__(sim, util, start, end)

class YourBot:
    def doAction(self, botActionsWrapper):
        sim = botActionsWrapper.getSim()
        if(sim != None):
            util = Util(sim)
            toBase = PathToPlayerBase(sim, util)
            # toBase.collectibles == sim.maxCollectibles or toBase.collectibles == util.numCollectiblesLeft:
            if True: 
                if toBase.move == Action.MoveUp:
                    actionsThisRound = botActionsWrapper.sendMoveUp()
                elif  toBase.move == Action.MoveDown:
                    actionsThisRound = botActionsWrapper.sendMoveDown()
                elif  toBase.move == Action.MoveLeft:
                    actionsThisRound = botActionsWrapper.sendMoveLeft()
                elif  toBase.move == Action.MoveRight:
                    actionsThisRound = botActionsWrapper.sendMoveRight()
            # else if there is 1 or more collectibles to be picked up
            #   move towards collectible closest to an enemy
            #else:
            #   start the next game
        time.sleep(1)

if __name__ == "__main__":
    bot = YourBot()
    while(1):
        bot.doAction(botActions.NetworkBot())