# puzzler2018

## Requirements
python 3.6.1 or greater
pipenv: https://pipenv.readthedocs.io/en/latest/

## Rules
1. Implement your bot in yourBot.py
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

### First steps
execute the following to install your dependencies and start a annoying-sounding aliens example game. you should hear sound and see a some alien space ships, which will automatically close when they get to your vehicle.
```
make && make test-visualizer
```

### Run server
this actually runs the simulation and has endpoints to control the simulation
```
make run-server
```

### Run visualizer
this shows the current state of the local server's simulation by hitting the endpoints of the server
```
make run-visualizer
```

### Run the enemy random movement bot as the player bot
```
make run-base-bot
```

### Run your own bot (see yourBot.py to implement. By default will just print 'implement me', stay in the same spot, and wait a second)
```
make run-your-bot
```

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
- [ ] Well understood images for all entities
- [X] Display Leaderboard after max number of rounds
