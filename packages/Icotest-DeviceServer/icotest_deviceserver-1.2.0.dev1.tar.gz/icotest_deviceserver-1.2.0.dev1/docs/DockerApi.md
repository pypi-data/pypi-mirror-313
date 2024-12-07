# DeviceServer.DockerApi

All URIs are relative to *http://localhost/DeviceServer*

Method | HTTP request | Description
------------- | ------------- | -------------
[**get_container_logs**](DockerApi.md#get_container_logs) | **GET** /docker/container/logs | GET a docker container&#39;s logs
[**get_docker_container_names**](DockerApi.md#get_docker_container_names) | **GET** /docker/containers | GET all docker containers


# **get_container_logs**
> file get_container_logs(container_name, timestamps=timestamps, from_datetime=from_datetime, to_datetime=to_datetime, tail=tail)

GET a docker container's logs

Returns a container's log

### Example

```python
from __future__ import print_function
import time
import DeviceServer
from DeviceServer.rest import ApiException
from pprint import pprint
# Defining the host is optional and defaults to http://localhost/DeviceServer
# See configuration.py for a list of all supported configuration parameters.
configuration = DeviceServer.Configuration(
    host = "http://localhost/DeviceServer"
)


# Enter a context with an instance of the API client
with DeviceServer.ApiClient() as api_client:
    # Create an instance of the API class
    api_instance = DeviceServer.DockerApi(api_client)
    container_name = 'container_name_example' # str | Container's name
timestamps = True # bool | Show timestamps (optional)
from_datetime = '2013-10-20T19:20:30+01:00' # datetime | Show logs since a given datetime (optional)
to_datetime = '2013-10-20T19:20:30+01:00' # datetime | Show logs that occurred before the given datetime (optional)
tail = 1000 # int | Show the most recent number of lines (optional) (default to 1000)

    try:
        # GET a docker container's logs
        api_response = api_instance.get_container_logs(container_name, timestamps=timestamps, from_datetime=from_datetime, to_datetime=to_datetime, tail=tail)
        pprint(api_response)
    except ApiException as e:
        print("Exception when calling DockerApi->get_container_logs: %s\n" % e)
```

### Parameters

Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **container_name** | **str**| Container&#39;s name | 
 **timestamps** | **bool**| Show timestamps | [optional] 
 **from_datetime** | **datetime**| Show logs since a given datetime | [optional] 
 **to_datetime** | **datetime**| Show logs that occurred before the given datetime | [optional] 
 **tail** | **int**| Show the most recent number of lines | [optional] [default to 1000]

### Return type

**file**

### Authorization

No authorization required

### HTTP request headers

 - **Content-Type**: Not defined
 - **Accept**: application/octet-stream

### HTTP response details
| Status code | Description | Response headers |
|-------------|-------------|------------------|
**200** | OK |  -  |
**400** | Bad Request |  -  |
**401** | Unauthorized |  -  |
**403** | Forbidden |  -  |
**404** | Not Found |  -  |
**500** | Internal Server Error |  -  |

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

# **get_docker_container_names**
> object get_docker_container_names()

GET all docker containers

Returns a list of all docker containers running on the host.

### Example

```python
from __future__ import print_function
import time
import DeviceServer
from DeviceServer.rest import ApiException
from pprint import pprint
# Defining the host is optional and defaults to http://localhost/DeviceServer
# See configuration.py for a list of all supported configuration parameters.
configuration = DeviceServer.Configuration(
    host = "http://localhost/DeviceServer"
)


# Enter a context with an instance of the API client
with DeviceServer.ApiClient() as api_client:
    # Create an instance of the API class
    api_instance = DeviceServer.DockerApi(api_client)
    
    try:
        # GET all docker containers
        api_response = api_instance.get_docker_container_names()
        pprint(api_response)
    except ApiException as e:
        print("Exception when calling DockerApi->get_docker_container_names: %s\n" % e)
```

### Parameters
This endpoint does not need any parameter.

### Return type

**object**

### Authorization

No authorization required

### HTTP request headers

 - **Content-Type**: Not defined
 - **Accept**: application/json

### HTTP response details
| Status code | Description | Response headers |
|-------------|-------------|------------------|
**200** | OK |  -  |
**201** | Created |  -  |
**400** | Bad Request |  -  |
**401** | Unauthorized |  -  |
**403** | Forbidden |  -  |
**404** | Not Found |  -  |
**500** | Internal Server Error |  -  |

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

