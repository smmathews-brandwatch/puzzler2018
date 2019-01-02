# Puzzler 2018

## Attributions
SVGs are from https://game-icons.net:
* Cyborg face icon by Delapouite (https://delapouite.com/) under CC BY 3.0
* Annexation icon by Cathelineau (https://game-icons.net/) under CC BY 3.0
* Cryo chamber icon by Delapouite (https://delapouite.com/) under CC BY 3.0

## Requirements
* python 3.6.1 or greater
* pipenv: https://pipenv.readthedocs.io/en/latest/

## Rules
1. Implement your bot anywhere you'd like using the 'http://127.0.0.1:5000/simulator/tick' endpoint and (optionally) the 'http://127.0.0.1:5000/simulator/new' endpoint. For your convenience, yourBot.py is available to give you a starting point and baseBot.py is available to see how the enemies work.
1. The entities will execute their actions in the order they're listed in the sim.board.entities list
1. The player's bot can't move on to a space occupied by another entity, except for a collectible the player is picking up
1. The player can't hold up more than 5 collectibles
1. When the player attempts to move on to their home base, they will instead deposit all their collectibles in their base
1. There is a limit to the number of frames in a round
1. There is a limit to the number of rounds before the final judgement
1. Your bot is judged on the avg, high, and low of the following:
   1. Score. This is the number of collectibles you rescued minus the number of collectibles you lost.
   1. Rescued. This is the number of collectibles you deposited in your base.
   1. Lost. This is the number of collectibles your enemy deposited in their base.

## Running

### Gotchas
On Mac, you may need to install https://www.anaconda.com/download/#macos so pythonw for python3 is available.
You may need to install pygame directly: `python3 -m pip install -U pygame --user` to get the visualizer working

### First steps
Execute the following to install your dependencies and start a annoying-sounding aliens example game. you should hear sound and see a some alien space ships, which will automatically close when they get to your vehicle.
```
make && make test-visualizer
```

### Run server
this actually runs the simulation and has endpoints to control the simulation
```
make && make run-server
```

### Print routes
print all available endpoints
```
make && make print-routes
```
At the time of this writing, that was:

Endpoint | Methods | Rule
-------- | ------- | ----
health | GET | /
new | POST | /simulator/new
scores | GET | /roundScores
state | GET | /simulator/state
tick | POST | /simulator/tick

### Run visualizer
this shows the current state of the local server's simulation by hitting the endpoints of the server
```
make && make run-visualizer
```

#### Interactive Mode
In addition to visualizing the current state of the simulator (and ending score summary), the visualizer can be used to interact with the server for testing. Press 'i' to toggle interactive mode
* Use the arrow keys to send a tick with all player bots going in that indicative direction. This uses the '/simulator/tick' endpoint.
* Use the 'r' button to go to the next round. This uses the '/simulator/new' endpoint

### Run the enemy random movement bot as the player bot
```
make && make run-base-bot
```

### Run your own bot (see yourBot.py/yourBot.js to implement. By default will just print 'implement me', stay in the same spot, and wait a second)
#### python
```
make && make run-your-bot
```
#### js
```
make install-js-bot && make run-your-js-bot
```

## Swagger Editor
https://editor.swagger.io/?url=https://raw.githubusercontent.com/smmathews-bw-boston/puzzler2018/master/swagger/swagger.yaml

## Requested Feature List
- [ ] Ability to demo top implementations
- [X] Run simulator/visualizer locally
- [X] Local Web api to control the bot
- [X] Move limit
- [X] Same number of collectibles, but random location and random starting position of enemies
- [X] Score = bot collected collectibles - enemy collected collectibles
- [X] Simulation mode, 1000 games run. Record all scores. 
- [X] 5 collectible carrying capacity, then must touch your base
- [X] Base bot to be used as a template
- [X] Well (ish) understood images for all entities
- [X] Display Leaderboard after max number of rounds

## Extra Challenges for bragging rights
1) Set simulator.ALLOW_STEALING to True. If you move in to an enemy, you'll take what they're holding. If they move in to you, they'll do likewise.
2) Change numEnemies=2 to greater than 2.
