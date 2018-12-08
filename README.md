# puzzler2018

## First steps
execute the following to start a annoying-sounding aliens example game. you should hear sound and see a some alien space ships, which will automatically close when they get to your vehicle.
```
make && make test-visualizer
```

## Run server
this actually runs the simulation and has endpoints to control the simulation
```
run-server
```

## Run visualizer
this shows the current state of the local server's simulation by hitting the endpoints of the server
```
run-visualizer
```

## Requested Feature List
- [ ] Ability to demo top 5 implementations
- [X] Run simulator/visualizer locally
- [ ] Local Web api to control the bot
- [ ] Time limit
- [ ] Same number of collectibles, but random location and random starting position of enemies
- [ ] Score = bot collected diamonds - enemy collected diamonds
- [ ] Simulation mode, 1000 games run. Record min score, max score, average score, and for each the random seed. 
- [ ] 5 diamond carrying capacity, then must touch your base
