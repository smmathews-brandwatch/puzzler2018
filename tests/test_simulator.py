import unittest
from simulator import *

class testTickRequests(unittest.TestCase):
    def testCannotMoveNonBots(self):
        sim = Simulator()
        entityIdsToAction = []
        seenIds = set()
        for entity in sim.board.entities:
            if(entity.boardPiece != BoardPiece.Bot):
                entityIdsToAction.append(EntityAction(id=entity.id, action=Action.MoveDown))
                seenIds.add(entity.id)
        result = sim.handleTickRequest(TickRequest(entityIdsToAction=entityIdsToAction))
        self.assertIsInstance(result, BadTick)
        self.assertEqual(len(result.badIds), len(seenIds))
        self.assertEqual(0, len(result.duplicateIds))
        for id in result.badIds:
            self.assertIn(id, seenIds)
    
    def testCanMoveBots(self):
        sim = Simulator()
        entityIdsToAction = []
        seenIds = set()
        for entity in sim.board.entities:
            if(entity.boardPiece == BoardPiece.Bot):
                entityIdsToAction.append(EntityAction(id=entity.id, action=Action.MoveDown))
                seenIds.add(entity.id)
        result = sim.handleTickRequest(TickRequest(entityIdsToAction=entityIdsToAction))
        self.assertIsInstance(result, TickResponse)