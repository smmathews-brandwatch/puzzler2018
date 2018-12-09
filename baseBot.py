import botActions, time, random

class BaseBot:
    def doAction(self):
        actions = [botActions.sendMoveDown, botActions.sendMoveUp, botActions.sendMoveLeft, botActions.sendMoveRight]
        action = actions[random.randint(0,len(actions)-1)]
        action()
        time.sleep(1) # sleep for a second so we can watch the dumb base bot

if __name__ == "__main__":
    bot = BaseBot()
    while(1):
        bot.doAction()