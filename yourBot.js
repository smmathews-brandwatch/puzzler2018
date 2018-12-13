var http = require('http');
var Puzzler2018 = require('puzzler_2018');

function runBot() {
  var apiInstance = new Puzzler2018.SimulatorApi();
  var gotSimulatorState = function(error, data, response) {
    if (error) {
      console.error(error);
    } else {
      console.log('API called successfully. Returned data: ' + JSON.stringify(data));
    }
    var opts = { 
      'body': new Puzzler2018.TickBase() // TickBase | 
    };
    apiInstance.postSimulatorTick(opts,gotTickResult)
  };
  var getSimulatorState = function getSimulatorState() {
    apiInstance.getSimulatorState(gotSimulatorState);
  }
  var gotTickResult = function(error, data, response) {
    if (error) {
      console.error(error);
    } else {
      console.log('API called successfully. Returned data: ' + JSON.stringify(data));
    }
    setTimeout(getSimulatorState, 1000);
  };
  apiInstance.getSimulatorState(gotSimulatorState);
}
runBot();