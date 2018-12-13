var http = require('http');
var Puzzler2018 = require('puzzler_2018');

function runBot() {
  var apiInstance = new Puzzler2018.SimulatorApi();
  var gotSimulatorState = function(error, data, response) {
    if (error) {
      console.error(error);
    } else {
      var tickRequest = new Puzzler2018.TickRequest();
      var entityAction = new Puzzler2018.EntityAction();
      entityAction.id = 0;// in a single player game the player's id is always zero, but we could find this in the data as well
      actions = [Puzzler2018.Action.up,Puzzler2018.Action.down,Puzzler2018.Action.left,Puzzler2018.Action.right]
      entityAction.action = Puzzler2018.Action.stay;
      // uncomment to move in a random direction
      //entityAction.action = actions[Math.floor(Math.random()*actions.length)];
      tickRequest.entityIdsToAction = [].concat(entityAction);
      apiInstance.postSimulatorTick(tickRequest,gotTickResult)
    }
  };
  var getSimulatorState = function getSimulatorState() {
    apiInstance.getSimulatorState(gotSimulatorState);
  }
  var gotTickResult = function(error, data, response) {
    if (error) {
      console.error(error);
    } else {
      // do something with the results of the tick (in data)
    }
    // call directly to avoid the 1 second timeout
    setTimeout(getSimulatorState, 1000);
  };
  apiInstance.getSimulatorState(gotSimulatorState);
}
runBot();