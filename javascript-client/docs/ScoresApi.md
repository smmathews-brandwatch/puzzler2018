# Puzzler2018.ScoresApi

All URIs are relative to *http://127.0.0.1:5000*

Method | HTTP request | Description
------------- | ------------- | -------------
[**getRoundScores**](ScoresApi.md#getRoundScores) | **GET** /roundScores | get all scores for all finished rounds


<a name="getRoundScores"></a>
# **getRoundScores**
> [Score] getRoundScores()

get all scores for all finished rounds

### Example
```javascript
var Puzzler2018 = require('puzzler_2018');

var apiInstance = new Puzzler2018.ScoresApi();

var callback = function(error, data, response) {
  if (error) {
    console.error(error);
  } else {
    console.log('API called successfully. Returned data: ' + data);
  }
};
apiInstance.getRoundScores(callback);
```

### Parameters
This endpoint does not need any parameter.

### Return type

[**[Score]**](Score.md)

### Authorization

No authorization required

### HTTP request headers

 - **Content-Type**: Not defined
 - **Accept**: application/json

