import botActions, time, random

class YourBot:
    def doAction(self, botActionsWrapper):
        # note a few things:
        # 1) The entities will execute their actions in the order they're listed in the sim.board.entities list
        # 2) The player's bot can't move on to a space occupied by another entity, except for a collectible the player is picking up
        # 3) The player can't hold up more than 5 collectibles
        # 4) When the player attempts to move on to their home base, they will instead deposit all their collectibles in their base
        # 5) There is a limit to the number of frames in a round
        # 6) There is a limit to the number of rounds before the final judgement
        # 7) Your bot is judged on the avg, high, and low of the following:
        #   a) Score. This is the number of collectibles you rescued minus the number of collectibles you lost.
        #   b) Rescued. This is the number of collectibles you deposited in your base.
        #   c) Lost. This is the number of collectibles your enemy deposited in their base.
        # below are your available actions
        #sim = botActionsWrapper.getSim()
        #actionsThisRound = botActionsWrapper.sendMoveDown
        #actionsThisRound = botActionsWrapper.sendMoveUp
        #actionsThisRound = botActionsWrapper.sendMoveLeft
        #actionsThisRound = botActionsWrapper.sendMoveRight
        actionsThisRound = botActionsWrapper.sendStay()
        print('implement me')
        # remove this sleep to run as fast as you can
        time.sleep(1)

if __name__ == "__main__":
    bot = YourBot()
    while(1):
        bot.doAction(botActions.NetworkBot())