# puzzler2018

## Requirements
python 3.6.1 or greater
pipenv: https://pipenv.readthedocs.io/en/latest/

## First steps
execute the following to start a annoying-sounding aliens example game. you should hear sound and see a some alien space ships, which will automatically close when they get to your vehicle.
```
make && make test-visualizer
```

## Run server
this actually runs the simulation and has endpoints to control the simulation
```
make run-server
```

## Run visualizer
this shows the current state of the local server's simulation by hitting the endpoints of the server
```
make run-visualizer
```

## Run the enemy random movement bot as the player bot
```
make run-base-bot
```

## Run your own bot (see yourBot.py to implement. By default will just print 'implement me')
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