# Puzzler2018.SimulatorApi

All URIs are relative to *http://127.0.0.1:5000*

Method | HTTP request | Description
------------- | ------------- | -------------
[**getSimulatorState**](SimulatorApi.md#getSimulatorState) | **GET** /simulator/state | Get the current state of the simulator
[**postSimulatorTick**](SimulatorApi.md#postSimulatorTick) | **POST** /simulator/tick | specify the bot&#39;s action for this frame
[**simulatorNewPost**](SimulatorApi.md#simulatorNewPost) | **POST** /simulator/new | record current score and skip to the next round


<a name="getSimulatorState"></a>
# **getSimulatorState**
> Object getSimulatorState()

Get the current state of the simulator

### Example
```javascript
var Puzzler2018 = require('puzzler_2018');

var apiInstance = new Puzzler2018.SimulatorApi();

var callback = function(error, data, response) {
  if (error) {
    console.error(error);
  } else {
    console.log('API called successfully. Returned data: ' + data);
  }
};
apiInstance.getSimulatorState(callback);
```

### Parameters
This endpoint does not need any parameter.

### Return type

**Object**

### Authorization

No authorization required

### HTTP request headers

 - **Content-Type**: Not defined
 - **Accept**: application/json

<a name="postSimulatorTick"></a>
# **postSimulatorTick**
> Simulator postSimulatorTick(body)

specify the bot&#39;s action for this frame

### Example
```javascript
var Puzzler2018 = require('puzzler_2018');

var apiInstance = new Puzzler2018.SimulatorApi();

var body = new Puzzler2018.TickBase(); // TickBase | 


var callback = function(error, data, response) {
  if (error) {
    console.error(error);
  } else {
    console.log('API called successfully. Returned data: ' + data);
  }
};
apiInstance.postSimulatorTick(body, callback);
```

### Parameters

Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **body** | [**TickBase**](TickBase.md)|  | 

### Return type

[**Simulator**](Simulator.md)

### Authorization

No authorization required

### HTTP request headers

 - **Content-Type**: application/json
 - **Accept**: application/json

<a name="simulatorNewPost"></a>
# **simulatorNewPost**
> simulatorNewPost()

record current score and skip to the next round

### Example
```javascript
var Puzzler2018 = require('puzzler_2018');

var apiInstance = new Puzzler2018.SimulatorApi();

var callback = function(error, data, response) {
  if (error) {
    console.error(error);
  } else {
    console.log('API called successfully.');
  }
};
apiInstance.simulatorNewPost(callback);
```

### Parameters
This endpoint does not need any parameter.

### Return type

null (empty response body)

### Authorization

No authorization required

### HTTP request headers

 - **Content-Type**: Not defined
 - **Accept**: Not defined

