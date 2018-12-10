import botActions, time, random

class BaseBot:
    def doAction(self, botActionsWrapper):
        actions = [botActionsWrapper.sendMoveDown, botActionsWrapper.sendMoveUp, botActionsWrapper.sendMoveLeft, botActionsWrapper.sendMoveRight]
        action = actions[random.randint(0,len(actions)-1)]
        action()

if __name__ == "__main__":
    bot = BaseBot()
    while(1):
        bot.doAction(botActions.NetworkBot())