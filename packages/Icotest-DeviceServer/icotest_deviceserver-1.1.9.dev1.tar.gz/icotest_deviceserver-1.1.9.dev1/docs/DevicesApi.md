# DeviceServer.DevicesApi

All URIs are relative to *http://localhost/DeviceServer*

Method | HTTP request | Description
------------- | ------------- | -------------
[**get_attenuator_state**](DevicesApi.md#get_attenuator_state) | **GET** /Devices/{device_id}/Attenuate | GET attenuation state
[**get_channel_attenuation**](DevicesApi.md#get_channel_attenuation) | **GET** /Devices/{device_id}/AttenuateChannel | GET attenuation channel state
[**get_current**](DevicesApi.md#get_current) | **GET** /Devices/{device_id}/Currents/{current_index} | GET current reading of device
[**get_device_attenuation_configuration**](DevicesApi.md#get_device_attenuation_configuration) | **GET** /Devices/{device_id}/AttenuatorConfig | GET attenuation device config
[**get_device_device_id_buttons**](DevicesApi.md#get_device_device_id_buttons) | **GET** /Devices/{device_id}/Buttons | GET all buttons for device
[**get_device_device_id_leds**](DevicesApi.md#get_device_device_id_leds) | **GET** /Devices/{device_id}/Leds | GET all leds for device
[**get_device_device_id_ports**](DevicesApi.md#get_device_device_id_ports) | **GET** /Devices/{device_id}/Ports | GET all ports for device
[**get_device_device_id_temperature_ports**](DevicesApi.md#get_device_device_id_temperature_ports) | **GET** /Devices/{device_id}/Temparatures | GET all temperature ports for device
[**get_device_id_port_index**](DevicesApi.md#get_device_id_port_index) | **GET** /Devices/{device_id}/Ports/{port_index} | GET status of port
[**get_device_led**](DevicesApi.md#get_device_led) | **GET** /Devices/{device_id}/Leds/{led_index} | GET state of LED
[**get_device_port_current**](DevicesApi.md#get_device_port_current) | **GET** /Devices/{device_id}/Ports/{port_index}/Currents | GET current reading of device Port
[**get_device_port_module_led_state**](DevicesApi.md#get_device_port_module_led_state) | **GET** /Devices/{device_id}/Ports/{port_index}/Modules/{module_index}/Leds | GET state of Port LED
[**get_device_port_module_relay_state**](DevicesApi.md#get_device_port_module_relay_state) | **GET** /Devices/{device_id}/Ports/{port_index}/Modules/{module_index}/Relays/{relay_index} | GET state of Port LED
[**get_device_port_voltage**](DevicesApi.md#get_device_port_voltage) | **GET** /Devices/{device_id}/Ports/{port_index}/Voltages | GET voltage reading of device Port
[**get_device_rotation_angle**](DevicesApi.md#get_device_rotation_angle) | **GET** /Devices/{device_id}/Rotation | GET Rotation Angle
[**get_device_rotation_speed**](DevicesApi.md#get_device_rotation_speed) | **GET** /Devices/{device_id}/Turntable/Speed | GET Turntable Speed
[**get_device_uuid**](DevicesApi.md#get_device_uuid) | **GET** /Serial/{device_serial} | GET uuid from database
[**get_devices**](DevicesApi.md#get_devices) | **GET** /Devices | GET list of devices
[**get_devices_button**](DevicesApi.md#get_devices_button) | **GET** /Devices/{device_id}/Button | GET state of button
[**get_devices_index**](DevicesApi.md#get_devices_index) | **GET** /Devices/{device_id} | GET single device
[**get_devices_temperature**](DevicesApi.md#get_devices_temperature) | **GET** /Devices/{device_id}/Temperature | GET temperature reading
[**get_fan_speed**](DevicesApi.md#get_fan_speed) | **GET** /Devices/{device_id}/Fan/{fan_index}/Speed | GET device fan speed
[**get_fan_target_temperature**](DevicesApi.md#get_fan_target_temperature) | **GET** /Devices/{device_id}/Fan/{fan_index}/TargetTemperature | GET device fan target temperature
[**get_fan_temperature**](DevicesApi.md#get_fan_temperature) | **GET** /Devices/{device_id}/Fan/{fan_index}/Temperature | GET device fan temperature
[**get_firmware_version**](DevicesApi.md#get_firmware_version) | **GET** /Devices/{device_id}/Firmware | GET Device Firmware Version
[**get_image**](DevicesApi.md#get_image) | **GET** /Devices/{device_id}/Turntable/Image | GET Image
[**get_image_names**](DevicesApi.md#get_image_names) | **GET** /Devices/{device_id}/Turntable/ImageNames | GET Image Names
[**get_message_from_rx_buffer**](DevicesApi.md#get_message_from_rx_buffer) | **GET** /Devices/messages/rx | GET message from RX table
[**get_message_from_tx_buffer**](DevicesApi.md#get_message_from_tx_buffer) | **GET** /Devices/messages/tx | GET message from TX table
[**get_port**](DevicesApi.md#get_port) | **GET** /Port/{port_id} | GET status of port by id
[**get_port_led_state**](DevicesApi.md#get_port_led_state) | **GET** /Devices/{device_id}/Ports/{port_index}/Leds/{led_index} | GET state of Port LED
[**get_port_setup_status**](DevicesApi.md#get_port_setup_status) | **GET** /Devices/{device_id}/Ports/{port_index}/SetupStatus | GET status of port
[**get_port_states**](DevicesApi.md#get_port_states) | **GET** /PortStates/{port_id} | GET port states by port id
[**get_ports**](DevicesApi.md#get_ports) | **GET** /Ports | GET status of all ports
[**get_relay_state**](DevicesApi.md#get_relay_state) | **GET** /Devices/{device_id}/Relay | GET state of relay
[**get_temperature_range**](DevicesApi.md#get_temperature_range) | **GET** /Devices/{device_id}/Temperature/Range | GET Temperature Range
[**get_temperature_thresholds**](DevicesApi.md#get_temperature_thresholds) | **GET** /Devices/{device_id}/Temperature/Thresholds | GET Temperature Thresholds
[**get_turntable_calibration_data**](DevicesApi.md#get_turntable_calibration_data) | **GET** /Devices/{device_id}/TurntableCalibration | GET Turntable Calibration Values
[**get_voltage**](DevicesApi.md#get_voltage) | **GET** /Devices/{device_id}/Voltages/{voltage_index} | GET voltage reading of device
[**put_attenuator_state**](DevicesApi.md#put_attenuator_state) | **PUT** /Devices/{device_id}/Attenuate | PUT attenuation state
[**put_auto_calibrate_turntable**](DevicesApi.md#put_auto_calibrate_turntable) | **PUT** /Devices/{device_id}/TurntableCalibration | PUT Calibration
[**put_channel_attenuation**](DevicesApi.md#put_channel_attenuation) | **PUT** /Devices/{device_id}/AttenuateChannel | PUT attenuation state
[**put_device**](DevicesApi.md#put_device) | **PUT** /Devices/AddDevice | PUT Add device
[**put_device_device_id_description**](DevicesApi.md#put_device_device_id_description) | **PUT** /Device/{device_id}/Description | PUT a description for a Device
[**put_device_device_id_name**](DevicesApi.md#put_device_device_id_name) | **PUT** /Device/{device_id}/Name | PUT a name for a Device
[**put_device_id_label**](DevicesApi.md#put_device_id_label) | **PUT** /Device/{device_id}/Port/{port_index}/Label | PUT a Port label
[**put_device_port_module_led_state**](DevicesApi.md#put_device_port_module_led_state) | **PUT** /Devices/{device_id}/Ports/{port_index}/Modules/{module_index}/Leds | PUT state of Port LED
[**put_device_port_module_relay_state**](DevicesApi.md#put_device_port_module_relay_state) | **PUT** /Devices/{device_id}/Ports/{port_index}/Modules/{module_index}/Relays/{relay_index} | PUT state of Port Relay
[**put_device_rotation_angle**](DevicesApi.md#put_device_rotation_angle) | **PUT** /Devices/{device_id}/Rotation | PUT Rotation
[**put_device_rotation_angle_continuous**](DevicesApi.md#put_device_rotation_angle_continuous) | **PUT** /Devices/{device_id}/ContiniousRotation | PUT Continious Rotation
[**put_device_rotation_speed**](DevicesApi.md#put_device_rotation_speed) | **PUT** /Devices/{device_id}/Turntable/Speed | PUT Turntable Speed
[**put_devices_led_index**](DevicesApi.md#put_devices_led_index) | **PUT** /Devices/{device_id}/Leds/{led_index} | PUT state of LED
[**put_devices_ports**](DevicesApi.md#put_devices_ports) | **PUT** /Devices/{device_id}/Ports/{port_index} | PUT state of port
[**put_halt_rotation**](DevicesApi.md#put_halt_rotation) | **PUT** /Devices/{device_id}/HaltRotation | PUT Halt Rotation
[**put_port_led_state**](DevicesApi.md#put_port_led_state) | **PUT** /Devices/{device_id}/Ports/{port_index}/Leds/{led_index} | PUT state of Port LED
[**put_port_port_id_label**](DevicesApi.md#put_port_port_id_label) | **PUT** /Port/{port_id}/Label | PUT the label for a Port
[**put_port_port_id_state_label**](DevicesApi.md#put_port_port_id_state_label) | **PUT** /Port/{port_id}/StateLabel | PUT state label
[**put_port_states_port_id**](DevicesApi.md#put_port_states_port_id) | **PUT** /PortStates/{port_id} | 
[**put_ports_pulse**](DevicesApi.md#put_ports_pulse) | **PUT** /Devices/{device_id}/Ports/{port_index}/Pulse | PUT port into state for period of time
[**put_relay_state**](DevicesApi.md#put_relay_state) | **PUT** /Devices/{device_id}/Relay | 
[**put_serial_test_message**](DevicesApi.md#put_serial_test_message) | **PUT** /Devices/{device_id}/Ports/{port_index}/SerialMessage | Serial Message Test
[**put_state_by_port_id**](DevicesApi.md#put_state_by_port_id) | **PUT** /Port/{port_id} | PUT state of port


# **get_attenuator_state**
> AttenuationState get_attenuator_state(device_id, expander_index, expander_port_index=expander_port_index)

GET attenuation state

Get attenuation state selected expander port

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
    api_instance = DeviceServer.DevicesApi(api_client)
    device_id = 'device_id_example' # str | 
expander_index = 56 # int | expander index
expander_port_index = 56 # int | expander port index (optional)

    try:
        # GET attenuation state
        api_response = api_instance.get_attenuator_state(device_id, expander_index, expander_port_index=expander_port_index)
        pprint(api_response)
    except ApiException as e:
        print("Exception when calling DevicesApi->get_attenuator_state: %s\n" % e)
```

### Parameters

Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **device_id** | **str**|  | 
 **expander_index** | **int**| expander index | 
 **expander_port_index** | **int**| expander port index | [optional] 

### Return type

[**AttenuationState**](AttenuationState.md)

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

# **get_channel_attenuation**
> ChannelAttenuationState get_channel_attenuation(device_id, channel_index)

GET attenuation channel state

Get attenuation state sof selected channel

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
    api_instance = DeviceServer.DevicesApi(api_client)
    device_id = 'device_id_example' # str | 
channel_index = 56 # int | channel index

    try:
        # GET attenuation channel state
        api_response = api_instance.get_channel_attenuation(device_id, channel_index)
        pprint(api_response)
    except ApiException as e:
        print("Exception when calling DevicesApi->get_channel_attenuation: %s\n" % e)
```

### Parameters

Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **device_id** | **str**|  | 
 **channel_index** | **int**| channel index | 

### Return type

[**ChannelAttenuationState**](ChannelAttenuationState.md)

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

# **get_current**
> float get_current(device_id, current_index)

GET current reading of device

Returns voltage reading on selected device. 

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
    api_instance = DeviceServer.DevicesApi(api_client)
    device_id = 'device_id_example' # str | UUID of device
current_index = 56 # int | Index of Current port

    try:
        # GET current reading of device
        api_response = api_instance.get_current(device_id, current_index)
        pprint(api_response)
    except ApiException as e:
        print("Exception when calling DevicesApi->get_current: %s\n" % e)
```

### Parameters

Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **device_id** | **str**| UUID of device | 
 **current_index** | **int**| Index of Current port | 

### Return type

**float**

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

# **get_device_attenuation_configuration**
> object get_device_attenuation_configuration(device_id)

GET attenuation device config

Get attenuation condig sent through by the device

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
    api_instance = DeviceServer.DevicesApi(api_client)
    device_id = 'device_id_example' # str | 

    try:
        # GET attenuation device config
        api_response = api_instance.get_device_attenuation_configuration(device_id)
        pprint(api_response)
    except ApiException as e:
        print("Exception when calling DevicesApi->get_device_attenuation_configuration: %s\n" % e)
```

### Parameters

Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **device_id** | **str**|  | 

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

# **get_device_device_id_buttons**
> list[DeviceButton] get_device_device_id_buttons(device_id)

GET all buttons for device

Returns a list of all buttons attached to a device.

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
    api_instance = DeviceServer.DevicesApi(api_client)
    device_id = 'device_id_example' # str | UUID of device

    try:
        # GET all buttons for device
        api_response = api_instance.get_device_device_id_buttons(device_id)
        pprint(api_response)
    except ApiException as e:
        print("Exception when calling DevicesApi->get_device_device_id_buttons: %s\n" % e)
```

### Parameters

Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **device_id** | **str**| UUID of device | 

### Return type

[**list[DeviceButton]**](DeviceButton.md)

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

# **get_device_device_id_leds**
> list[DeviceLed] get_device_device_id_leds(device_id)

GET all leds for device

Returns a list of all buttons attached to a device.

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
    api_instance = DeviceServer.DevicesApi(api_client)
    device_id = 'device_id_example' # str | UUID of device

    try:
        # GET all leds for device
        api_response = api_instance.get_device_device_id_leds(device_id)
        pprint(api_response)
    except ApiException as e:
        print("Exception when calling DevicesApi->get_device_device_id_leds: %s\n" % e)
```

### Parameters

Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **device_id** | **str**| UUID of device | 

### Return type

[**list[DeviceLed]**](DeviceLed.md)

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

# **get_device_device_id_ports**
> list[DevicePort] get_device_device_id_ports(device_id)

GET all ports for device

Returns a list of all ports attached to a device.

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
    api_instance = DeviceServer.DevicesApi(api_client)
    device_id = 'device_id_example' # str | UUID of device

    try:
        # GET all ports for device
        api_response = api_instance.get_device_device_id_ports(device_id)
        pprint(api_response)
    except ApiException as e:
        print("Exception when calling DevicesApi->get_device_device_id_ports: %s\n" % e)
```

### Parameters

Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **device_id** | **str**| UUID of device | 

### Return type

[**list[DevicePort]**](DevicePort.md)

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

# **get_device_device_id_temperature_ports**
> list[DeviceTemperaturePort] get_device_device_id_temperature_ports(device_id)

GET all temperature ports for device

Returns a list of all temperature ports attached to a device.

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
    api_instance = DeviceServer.DevicesApi(api_client)
    device_id = 'device_id_example' # str | UUID of device

    try:
        # GET all temperature ports for device
        api_response = api_instance.get_device_device_id_temperature_ports(device_id)
        pprint(api_response)
    except ApiException as e:
        print("Exception when calling DevicesApi->get_device_device_id_temperature_ports: %s\n" % e)
```

### Parameters

Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **device_id** | **str**| UUID of device | 

### Return type

[**list[DeviceTemperaturePort]**](DeviceTemperaturePort.md)

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

# **get_device_id_port_index**
> DevicePort get_device_id_port_index(device_id, port_index)

GET status of port

Returns status of ports.

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
    api_instance = DeviceServer.DevicesApi(api_client)
    device_id = 'device_id_example' # str | UUID of device
port_index = 56 # int | Index of port

    try:
        # GET status of port
        api_response = api_instance.get_device_id_port_index(device_id, port_index)
        pprint(api_response)
    except ApiException as e:
        print("Exception when calling DevicesApi->get_device_id_port_index: %s\n" % e)
```

### Parameters

Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **device_id** | **str**| UUID of device | 
 **port_index** | **int**| Index of port | 

### Return type

[**DevicePort**](DevicePort.md)

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

# **get_device_led**
> LedState get_device_led(device_id, led_index)

GET state of LED

Returns state of selected led on selected device

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
    api_instance = DeviceServer.DevicesApi(api_client)
    device_id = 'device_id_example' # str | UUID of device
led_index = 56 # int | Index of LED

    try:
        # GET state of LED
        api_response = api_instance.get_device_led(device_id, led_index)
        pprint(api_response)
    except ApiException as e:
        print("Exception when calling DevicesApi->get_device_led: %s\n" % e)
```

### Parameters

Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **device_id** | **str**| UUID of device | 
 **led_index** | **int**| Index of LED | 

### Return type

[**LedState**](LedState.md)

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

# **get_device_port_current**
> float get_device_port_current(device_id, port_index)

GET current reading of device Port

Returns current reading on selected device port 

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
    api_instance = DeviceServer.DevicesApi(api_client)
    device_id = 'device_id_example' # str | UUID of device
port_index = 56 # int | Port Index

    try:
        # GET current reading of device Port
        api_response = api_instance.get_device_port_current(device_id, port_index)
        pprint(api_response)
    except ApiException as e:
        print("Exception when calling DevicesApi->get_device_port_current: %s\n" % e)
```

### Parameters

Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **device_id** | **str**| UUID of device | 
 **port_index** | **int**| Port Index | 

### Return type

**float**

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

# **get_device_port_module_led_state**
> object get_device_port_module_led_state(device_id, port_index, module_index)

GET state of Port LED

Returns state of selected led on specified device's port's module

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
    api_instance = DeviceServer.DevicesApi(api_client)
    device_id = 'device_id_example' # str | UUID of device
port_index = 56 # int | Index of Port
module_index = 56 # int | Index of Module

    try:
        # GET state of Port LED
        api_response = api_instance.get_device_port_module_led_state(device_id, port_index, module_index)
        pprint(api_response)
    except ApiException as e:
        print("Exception when calling DevicesApi->get_device_port_module_led_state: %s\n" % e)
```

### Parameters

Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **device_id** | **str**| UUID of device | 
 **port_index** | **int**| Index of Port | 
 **module_index** | **int**| Index of Module | 

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

# **get_device_port_module_relay_state**
> object get_device_port_module_relay_state(device_id, port_index, module_index, relay_index)

GET state of Port LED

Returns state of selected relay on specified device's port's module

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
    api_instance = DeviceServer.DevicesApi(api_client)
    device_id = 'device_id_example' # str | UUID of device
port_index = 56 # int | Index of Port
module_index = 56 # int | Index of Module
relay_index = 56 # int | Index of Relay

    try:
        # GET state of Port LED
        api_response = api_instance.get_device_port_module_relay_state(device_id, port_index, module_index, relay_index)
        pprint(api_response)
    except ApiException as e:
        print("Exception when calling DevicesApi->get_device_port_module_relay_state: %s\n" % e)
```

### Parameters

Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **device_id** | **str**| UUID of device | 
 **port_index** | **int**| Index of Port | 
 **module_index** | **int**| Index of Module | 
 **relay_index** | **int**| Index of Relay | 

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

# **get_device_port_voltage**
> float get_device_port_voltage(device_id, port_index)

GET voltage reading of device Port

Returns voltage reading on selected device port

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
    api_instance = DeviceServer.DevicesApi(api_client)
    device_id = 'device_id_example' # str | UUID of device
port_index = 56 # int | Port Index

    try:
        # GET voltage reading of device Port
        api_response = api_instance.get_device_port_voltage(device_id, port_index)
        pprint(api_response)
    except ApiException as e:
        print("Exception when calling DevicesApi->get_device_port_voltage: %s\n" % e)
```

### Parameters

Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **device_id** | **str**| UUID of device | 
 **port_index** | **int**| Port Index | 

### Return type

**float**

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

# **get_device_rotation_angle**
> object get_device_rotation_angle(device_id)

GET Rotation Angle

Get the rotation angle of the turntable

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
    api_instance = DeviceServer.DevicesApi(api_client)
    device_id = 'device_id_example' # str | 

    try:
        # GET Rotation Angle
        api_response = api_instance.get_device_rotation_angle(device_id)
        pprint(api_response)
    except ApiException as e:
        print("Exception when calling DevicesApi->get_device_rotation_angle: %s\n" % e)
```

### Parameters

Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **device_id** | **str**|  | 

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

# **get_device_rotation_speed**
> object get_device_rotation_speed(device_id)

GET Turntable Speed

Get the configured turntable speed

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
    api_instance = DeviceServer.DevicesApi(api_client)
    device_id = 'device_id_example' # str | 

    try:
        # GET Turntable Speed
        api_response = api_instance.get_device_rotation_speed(device_id)
        pprint(api_response)
    except ApiException as e:
        print("Exception when calling DevicesApi->get_device_rotation_speed: %s\n" % e)
```

### Parameters

Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **device_id** | **str**|  | 

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

# **get_device_uuid**
> object get_device_uuid(device_serial)

GET uuid from database

Query database for device_id with device_serial and device_type

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
    api_instance = DeviceServer.DevicesApi(api_client)
    device_serial = 'device_serial_example' # str | Serial number of device

    try:
        # GET uuid from database
        api_response = api_instance.get_device_uuid(device_serial)
        pprint(api_response)
    except ApiException as e:
        print("Exception when calling DevicesApi->get_device_uuid: %s\n" % e)
```

### Parameters

Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **device_serial** | **str**| Serial number of device | 

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

# **get_devices**
> list[Device] get_devices()

GET list of devices

Returns list of devices

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
    api_instance = DeviceServer.DevicesApi(api_client)
    
    try:
        # GET list of devices
        api_response = api_instance.get_devices()
        pprint(api_response)
    except ApiException as e:
        print("Exception when calling DevicesApi->get_devices: %s\n" % e)
```

### Parameters
This endpoint does not need any parameter.

### Return type

[**list[Device]**](Device.md)

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

# **get_devices_button**
> ButtonState get_devices_button(device_id, button_index)

GET state of button

Returns state of the selected devices button

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
    api_instance = DeviceServer.DevicesApi(api_client)
    device_id = 'device_id_example' # str | UUID of device
button_index = 56 # int | Index of the button on tha device (1-100)

    try:
        # GET state of button
        api_response = api_instance.get_devices_button(device_id, button_index)
        pprint(api_response)
    except ApiException as e:
        print("Exception when calling DevicesApi->get_devices_button: %s\n" % e)
```

### Parameters

Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **device_id** | **str**| UUID of device | 
 **button_index** | **int**| Index of the button on tha device (1-100) | 

### Return type

[**ButtonState**](ButtonState.md)

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

# **get_devices_index**
> Device get_devices_index(device_id)

GET single device

Gets information for a single device.

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
    api_instance = DeviceServer.DevicesApi(api_client)
    device_id = 'device_id_example' # str | UUID of device

    try:
        # GET single device
        api_response = api_instance.get_devices_index(device_id)
        pprint(api_response)
    except ApiException as e:
        print("Exception when calling DevicesApi->get_devices_index: %s\n" % e)
```

### Parameters

Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **device_id** | **str**| UUID of device | 

### Return type

[**Device**](Device.md)

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

# **get_devices_temperature**
> float get_devices_temperature(device_id, thermometer_index=thermometer_index)

GET temperature reading

Get temperature reading from specified device

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
    api_instance = DeviceServer.DevicesApi(api_client)
    device_id = 'device_id_example' # str | 
thermometer_index = 56 # int | Index of the thermometer (1-7) (optional)

    try:
        # GET temperature reading
        api_response = api_instance.get_devices_temperature(device_id, thermometer_index=thermometer_index)
        pprint(api_response)
    except ApiException as e:
        print("Exception when calling DevicesApi->get_devices_temperature: %s\n" % e)
```

### Parameters

Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **device_id** | **str**|  | 
 **thermometer_index** | **int**| Index of the thermometer (1-7) | [optional] 

### Return type

**float**

### Authorization

No authorization required

### HTTP request headers

 - **Content-Type**: Not defined
 - **Accept**: application/json

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

# **get_fan_speed**
> object get_fan_speed(device_id, fan_index)

GET device fan speed

Get the fan speed of the selected index 

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
    api_instance = DeviceServer.DevicesApi(api_client)
    device_id = 'device_id_example' # str | 
fan_index = 'fan_index_example' # str | 

    try:
        # GET device fan speed
        api_response = api_instance.get_fan_speed(device_id, fan_index)
        pprint(api_response)
    except ApiException as e:
        print("Exception when calling DevicesApi->get_fan_speed: %s\n" % e)
```

### Parameters

Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **device_id** | **str**|  | 
 **fan_index** | **str**|  | 

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

# **get_fan_target_temperature**
> object get_fan_target_temperature(device_id, fan_index)

GET device fan target temperature

Get the fan target temeprature of the selected index 

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
    api_instance = DeviceServer.DevicesApi(api_client)
    device_id = 'device_id_example' # str | 
fan_index = 'fan_index_example' # str | 

    try:
        # GET device fan target temperature
        api_response = api_instance.get_fan_target_temperature(device_id, fan_index)
        pprint(api_response)
    except ApiException as e:
        print("Exception when calling DevicesApi->get_fan_target_temperature: %s\n" % e)
```

### Parameters

Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **device_id** | **str**|  | 
 **fan_index** | **str**|  | 

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

# **get_fan_temperature**
> object get_fan_temperature(device_id, fan_index)

GET device fan temperature

Get the fan temperature of the selected index 

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
    api_instance = DeviceServer.DevicesApi(api_client)
    device_id = 'device_id_example' # str | 
fan_index = 'fan_index_example' # str | 

    try:
        # GET device fan temperature
        api_response = api_instance.get_fan_temperature(device_id, fan_index)
        pprint(api_response)
    except ApiException as e:
        print("Exception when calling DevicesApi->get_fan_temperature: %s\n" % e)
```

### Parameters

Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **device_id** | **str**|  | 
 **fan_index** | **str**|  | 

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

# **get_firmware_version**
> FirmwareVersion get_firmware_version(device_id)

GET Device Firmware Version

Get the device firmware version.

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
    api_instance = DeviceServer.DevicesApi(api_client)
    device_id = 'device_id_example' # str | Device ID

    try:
        # GET Device Firmware Version
        api_response = api_instance.get_firmware_version(device_id)
        pprint(api_response)
    except ApiException as e:
        print("Exception when calling DevicesApi->get_firmware_version: %s\n" % e)
```

### Parameters

Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **device_id** | **str**| Device ID | 

### Return type

[**FirmwareVersion**](FirmwareVersion.md)

### Authorization

No authorization required

### HTTP request headers

 - **Content-Type**: Not defined
 - **Accept**: application/json

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

# **get_image**
> file get_image(device_id, image_name=image_name)

GET Image

Get the image from the provided name.

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
    api_instance = DeviceServer.DevicesApi(api_client)
    device_id = 'device_id_example' # str | 
image_name = 'image_name_example' # str | Image Name (optional)

    try:
        # GET Image
        api_response = api_instance.get_image(device_id, image_name=image_name)
        pprint(api_response)
    except ApiException as e:
        print("Exception when calling DevicesApi->get_image: %s\n" % e)
```

### Parameters

Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **device_id** | **str**|  | 
 **image_name** | **str**| Image Name | [optional] 

### Return type

**file**

### Authorization

No authorization required

### HTTP request headers

 - **Content-Type**: Not defined
 - **Accept**: image/png, application/json

### HTTP response details
| Status code | Description | Response headers |
|-------------|-------------|------------------|
**200** | OK |  -  |
**201** | Created |  -  |
**400** | Bad Request |  -  |
**404** | Not Found |  -  |
**500** | Internal Server Error |  -  |

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

# **get_image_names**
> object get_image_names(device_id)

GET Image Names

Get the image names available on the device.

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
    api_instance = DeviceServer.DevicesApi(api_client)
    device_id = 'device_id_example' # str | 

    try:
        # GET Image Names
        api_response = api_instance.get_image_names(device_id)
        pprint(api_response)
    except ApiException as e:
        print("Exception when calling DevicesApi->get_image_names: %s\n" % e)
```

### Parameters

Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **device_id** | **str**|  | 

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
**404** | Not Found |  -  |
**500** | Internal Server Error |  -  |

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

# **get_message_from_rx_buffer**
> object get_message_from_rx_buffer(device_id=device_id)

GET message from RX table

GET a message from the rx table

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
    api_instance = DeviceServer.DevicesApi(api_client)
    device_id = 'device_id_example' # str |  (optional)

    try:
        # GET message from RX table
        api_response = api_instance.get_message_from_rx_buffer(device_id=device_id)
        pprint(api_response)
    except ApiException as e:
        print("Exception when calling DevicesApi->get_message_from_rx_buffer: %s\n" % e)
```

### Parameters

Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **device_id** | **str**|  | [optional] 

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

# **get_message_from_tx_buffer**
> str get_message_from_tx_buffer(device_id=device_id, device_serial=device_serial, device_type=device_type)

GET message from TX table

GET a message from the tx table

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
    api_instance = DeviceServer.DevicesApi(api_client)
    device_id = 'device_id_example' # str |  (optional)
device_serial = 'device_serial_example' # str |  (optional)
device_type = 'device_type_example' # str |  (optional)

    try:
        # GET message from TX table
        api_response = api_instance.get_message_from_tx_buffer(device_id=device_id, device_serial=device_serial, device_type=device_type)
        pprint(api_response)
    except ApiException as e:
        print("Exception when calling DevicesApi->get_message_from_tx_buffer: %s\n" % e)
```

### Parameters

Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **device_id** | **str**|  | [optional] 
 **device_serial** | **str**|  | [optional] 
 **device_type** | **str**|  | [optional] 

### Return type

**str**

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

# **get_port**
> DevicePort get_port(port_id)

GET status of port by id

returns status of port

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
    api_instance = DeviceServer.DevicesApi(api_client)
    port_id = 'port_id_example' # str | id of port to set

    try:
        # GET status of port by id
        api_response = api_instance.get_port(port_id)
        pprint(api_response)
    except ApiException as e:
        print("Exception when calling DevicesApi->get_port: %s\n" % e)
```

### Parameters

Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **port_id** | **str**| id of port to set | 

### Return type

[**DevicePort**](DevicePort.md)

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

# **get_port_led_state**
> LedState get_port_led_state(device_id, port_index, led_index)

GET state of Port LED

Returns state of selected led on specified device's port

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
    api_instance = DeviceServer.DevicesApi(api_client)
    device_id = 'device_id_example' # str | UUID of device
port_index = 56 # int | Index of Port
led_index = 56 # int | Index of Led

    try:
        # GET state of Port LED
        api_response = api_instance.get_port_led_state(device_id, port_index, led_index)
        pprint(api_response)
    except ApiException as e:
        print("Exception when calling DevicesApi->get_port_led_state: %s\n" % e)
```

### Parameters

Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **device_id** | **str**| UUID of device | 
 **port_index** | **int**| Index of Port | 
 **led_index** | **int**| Index of Led | 

### Return type

[**LedState**](LedState.md)

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

# **get_port_setup_status**
> object get_port_setup_status(device_id, port_index)

GET status of port

Returns setup and connection status of port

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
    api_instance = DeviceServer.DevicesApi(api_client)
    device_id = 'device_id_example' # str | UUID of device
port_index = 56 # int | Index of port

    try:
        # GET status of port
        api_response = api_instance.get_port_setup_status(device_id, port_index)
        pprint(api_response)
    except ApiException as e:
        print("Exception when calling DevicesApi->get_port_setup_status: %s\n" % e)
```

### Parameters

Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **device_id** | **str**| UUID of device | 
 **port_index** | **int**| Index of port | 

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

# **get_port_states**
> list[PortState] get_port_states(port_id)

GET port states by port id

Gets a list of available port states for a port

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
    api_instance = DeviceServer.DevicesApi(api_client)
    port_id = 'port_id_example' # str | 

    try:
        # GET port states by port id
        api_response = api_instance.get_port_states(port_id)
        pprint(api_response)
    except ApiException as e:
        print("Exception when calling DevicesApi->get_port_states: %s\n" % e)
```

### Parameters

Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **port_id** | **str**|  | 

### Return type

[**list[PortState]**](PortState.md)

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

# **get_ports**
> list[DevicePort] get_ports()

GET status of all ports

status of port

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
    api_instance = DeviceServer.DevicesApi(api_client)
    
    try:
        # GET status of all ports
        api_response = api_instance.get_ports()
        pprint(api_response)
    except ApiException as e:
        print("Exception when calling DevicesApi->get_ports: %s\n" % e)
```

### Parameters
This endpoint does not need any parameter.

### Return type

[**list[DevicePort]**](DevicePort.md)

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

# **get_relay_state**
> RelayState get_relay_state(device_id, index)

GET state of relay

Get state of relay at index

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
    api_instance = DeviceServer.DevicesApi(api_client)
    device_id = 'device_id_example' # str | 
index = 56 # int | index of relay to get state of

    try:
        # GET state of relay
        api_response = api_instance.get_relay_state(device_id, index)
        pprint(api_response)
    except ApiException as e:
        print("Exception when calling DevicesApi->get_relay_state: %s\n" % e)
```

### Parameters

Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **device_id** | **str**|  | 
 **index** | **int**| index of relay to get state of | 

### Return type

[**RelayState**](RelayState.md)

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

# **get_temperature_range**
> TempRange get_temperature_range(device_id)

GET Temperature Range

Get the minimum and maximum temperatures for a given hex thermometer

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
    api_instance = DeviceServer.DevicesApi(api_client)
    device_id = 'device_id_example' # str | 

    try:
        # GET Temperature Range
        api_response = api_instance.get_temperature_range(device_id)
        pprint(api_response)
    except ApiException as e:
        print("Exception when calling DevicesApi->get_temperature_range: %s\n" % e)
```

### Parameters

Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **device_id** | **str**|  | 

### Return type

[**TempRange**](TempRange.md)

### Authorization

No authorization required

### HTTP request headers

 - **Content-Type**: Not defined
 - **Accept**: application/json

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

# **get_temperature_thresholds**
> list[float] get_temperature_thresholds(device_id)

GET Temperature Thresholds

get the points at which the temperature enters danger zones

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
    api_instance = DeviceServer.DevicesApi(api_client)
    device_id = 'device_id_example' # str | the device id

    try:
        # GET Temperature Thresholds
        api_response = api_instance.get_temperature_thresholds(device_id)
        pprint(api_response)
    except ApiException as e:
        print("Exception when calling DevicesApi->get_temperature_thresholds: %s\n" % e)
```

### Parameters

Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **device_id** | **str**| the device id | 

### Return type

**list[float]**

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

# **get_turntable_calibration_data**
> object get_turntable_calibration_data(device_id)

GET Turntable Calibration Values

Get the calibration data for the device

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
    api_instance = DeviceServer.DevicesApi(api_client)
    device_id = 'device_id_example' # str | 

    try:
        # GET Turntable Calibration Values
        api_response = api_instance.get_turntable_calibration_data(device_id)
        pprint(api_response)
    except ApiException as e:
        print("Exception when calling DevicesApi->get_turntable_calibration_data: %s\n" % e)
```

### Parameters

Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **device_id** | **str**|  | 

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

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

# **get_voltage**
> float get_voltage(device_id, voltage_index, voltage_index2=voltage_index2)

GET voltage reading of device

Returns voltage reading on selected device 

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
    api_instance = DeviceServer.DevicesApi(api_client)
    device_id = 'device_id_example' # str | UUID of device
voltage_index = 56 # int | Index of Voltage port
voltage_index2 = 'voltage_index_example' # str | Voltage index to query (optional)

    try:
        # GET voltage reading of device
        api_response = api_instance.get_voltage(device_id, voltage_index, voltage_index2=voltage_index2)
        pprint(api_response)
    except ApiException as e:
        print("Exception when calling DevicesApi->get_voltage: %s\n" % e)
```

### Parameters

Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **device_id** | **str**| UUID of device | 
 **voltage_index** | **int**| Index of Voltage port | 
 **voltage_index2** | **str**| Voltage index to query | [optional] 

### Return type

**float**

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

# **put_attenuator_state**
> put_attenuator_state(device_id, expander_index, expander_port_index, value)

PUT attenuation state

Get attenuation state selected expander port

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
    api_instance = DeviceServer.DevicesApi(api_client)
    device_id = 'device_id_example' # str | 
expander_index = 56 # int | expander index
expander_port_index = 56 # int | expander port
value = 56 # int | attenuation value

    try:
        # PUT attenuation state
        api_instance.put_attenuator_state(device_id, expander_index, expander_port_index, value)
    except ApiException as e:
        print("Exception when calling DevicesApi->put_attenuator_state: %s\n" % e)
```

### Parameters

Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **device_id** | **str**|  | 
 **expander_index** | **int**| expander index | 
 **expander_port_index** | **int**| expander port | 
 **value** | **int**| attenuation value | 

### Return type

void (empty response body)

### Authorization

No authorization required

### HTTP request headers

 - **Content-Type**: Not defined
 - **Accept**: Not defined

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

# **put_auto_calibrate_turntable**
> put_auto_calibrate_turntable(device_id)

PUT Calibration

1 Click auto-calibration, before execution ensure physical zero.

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
    api_instance = DeviceServer.DevicesApi(api_client)
    device_id = 'device_id_example' # str | 

    try:
        # PUT Calibration
        api_instance.put_auto_calibrate_turntable(device_id)
    except ApiException as e:
        print("Exception when calling DevicesApi->put_auto_calibrate_turntable: %s\n" % e)
```

### Parameters

Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **device_id** | **str**|  | 

### Return type

void (empty response body)

### Authorization

No authorization required

### HTTP request headers

 - **Content-Type**: Not defined
 - **Accept**: Not defined

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

# **put_channel_attenuation**
> put_channel_attenuation(device_id, channel_index, value)

PUT attenuation state

Put attenuation state of selected channel

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
    api_instance = DeviceServer.DevicesApi(api_client)
    device_id = 'device_id_example' # str | 
channel_index = 56 # int | channel index
value = 56 # int | attenuation value

    try:
        # PUT attenuation state
        api_instance.put_channel_attenuation(device_id, channel_index, value)
    except ApiException as e:
        print("Exception when calling DevicesApi->put_channel_attenuation: %s\n" % e)
```

### Parameters

Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **device_id** | **str**|  | 
 **channel_index** | **int**| channel index | 
 **value** | **int**| attenuation value | 

### Return type

void (empty response body)

### Authorization

No authorization required

### HTTP request headers

 - **Content-Type**: Not defined
 - **Accept**: Not defined

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

# **put_device**
> put_device(device_id=device_id, config_file_name=config_file_name, device_serial=device_serial)

PUT Add device

Add device to database

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
    api_instance = DeviceServer.DevicesApi(api_client)
    device_id = 'device_id_example' # str | Device UUID (optional)
config_file_name = 'config_file_name_example' # str | Config file name (optional)
device_serial = 'device_serial_example' # str | Device Serial (optional)

    try:
        # PUT Add device
        api_instance.put_device(device_id=device_id, config_file_name=config_file_name, device_serial=device_serial)
    except ApiException as e:
        print("Exception when calling DevicesApi->put_device: %s\n" % e)
```

### Parameters

Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **device_id** | **str**| Device UUID | [optional] 
 **config_file_name** | **str**| Config file name | [optional] 
 **device_serial** | **str**| Device Serial | [optional] 

### Return type

void (empty response body)

### Authorization

No authorization required

### HTTP request headers

 - **Content-Type**: Not defined
 - **Accept**: Not defined

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

# **put_device_device_id_description**
> put_device_device_id_description(device_id, description)

PUT a description for a Device

Set Description of the Device hosting ports 

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
    api_instance = DeviceServer.DevicesApi(api_client)
    device_id = 'e93a8ad5-c8dc-4069-8097-13feb8af9b65' # str | 
description = 'description_example' # str | 

    try:
        # PUT a description for a Device
        api_instance.put_device_device_id_description(device_id, description)
    except ApiException as e:
        print("Exception when calling DevicesApi->put_device_device_id_description: %s\n" % e)
```

### Parameters

Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **device_id** | **str**|  | 
 **description** | **str**|  | 

### Return type

void (empty response body)

### Authorization

No authorization required

### HTTP request headers

 - **Content-Type**: Not defined
 - **Accept**: Not defined

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

# **put_device_device_id_name**
> put_device_device_id_name(device_id, name)

PUT a name for a Device

set name of device

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
    api_instance = DeviceServer.DevicesApi(api_client)
    device_id = 'device_id_example' # str | id of device 
name = 'name_example' # str | name to apply to device

    try:
        # PUT a name for a Device
        api_instance.put_device_device_id_name(device_id, name)
    except ApiException as e:
        print("Exception when calling DevicesApi->put_device_device_id_name: %s\n" % e)
```

### Parameters

Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **device_id** | **str**| id of device  | 
 **name** | **str**| name to apply to device | 

### Return type

void (empty response body)

### Authorization

No authorization required

### HTTP request headers

 - **Content-Type**: Not defined
 - **Accept**: Not defined

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

# **put_device_id_label**
> put_device_id_label(device_id, port_index, label)

PUT a Port label

Sets the label used for a port

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
    api_instance = DeviceServer.DevicesApi(api_client)
    device_id = 'device_id_example' # str | 
port_index = 56 # int | 
label = 'Example lable' # str | new label for port

    try:
        # PUT a Port label
        api_instance.put_device_id_label(device_id, port_index, label)
    except ApiException as e:
        print("Exception when calling DevicesApi->put_device_id_label: %s\n" % e)
```

### Parameters

Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **device_id** | **str**|  | 
 **port_index** | **int**|  | 
 **label** | **str**| new label for port | 

### Return type

void (empty response body)

### Authorization

No authorization required

### HTTP request headers

 - **Content-Type**: Not defined
 - **Accept**: Not defined

### HTTP response details
| Status code | Description | Response headers |
|-------------|-------------|------------------|
**200** | OK |  -  |
**400** | Bad Request |  -  |
**403** | Forbidden |  -  |
**404** | Not Found |  -  |
**500** | Internal Server Error |  -  |

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

# **put_device_port_module_led_state**
> put_device_port_module_led_state(device_id, port_index, module_index, state)

PUT state of Port LED

Set led at index on specified device's port

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
    api_instance = DeviceServer.DevicesApi(api_client)
    device_id = 'device_id_example' # str | UUID of device
port_index = 56 # int | Index of Port
module_index = 56 # int | Index of Module
state = True # bool | True = LED on, False = LED off

    try:
        # PUT state of Port LED
        api_instance.put_device_port_module_led_state(device_id, port_index, module_index, state)
    except ApiException as e:
        print("Exception when calling DevicesApi->put_device_port_module_led_state: %s\n" % e)
```

### Parameters

Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **device_id** | **str**| UUID of device | 
 **port_index** | **int**| Index of Port | 
 **module_index** | **int**| Index of Module | 
 **state** | **bool**| True &#x3D; LED on, False &#x3D; LED off | 

### Return type

void (empty response body)

### Authorization

No authorization required

### HTTP request headers

 - **Content-Type**: Not defined
 - **Accept**: Not defined

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

# **put_device_port_module_relay_state**
> put_device_port_module_relay_state(device_id, port_index, module_index, relay_index, state)

PUT state of Port Relay

Set relay at index on specified device's port's module

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
    api_instance = DeviceServer.DevicesApi(api_client)
    device_id = 'device_id_example' # str | UUID of device
port_index = 56 # int | Index of Port
module_index = 56 # int | Index of Module
relay_index = 56 # int | Index of Relay
state = True # bool | True = LED on, False = LED off

    try:
        # PUT state of Port Relay
        api_instance.put_device_port_module_relay_state(device_id, port_index, module_index, relay_index, state)
    except ApiException as e:
        print("Exception when calling DevicesApi->put_device_port_module_relay_state: %s\n" % e)
```

### Parameters

Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **device_id** | **str**| UUID of device | 
 **port_index** | **int**| Index of Port | 
 **module_index** | **int**| Index of Module | 
 **relay_index** | **int**| Index of Relay | 
 **state** | **bool**| True &#x3D; LED on, False &#x3D; LED off | 

### Return type

void (empty response body)

### Authorization

No authorization required

### HTTP request headers

 - **Content-Type**: Not defined
 - **Accept**: Not defined

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

# **put_device_rotation_angle**
> put_device_rotation_angle(device_id, target_angle)

PUT Rotation

Put rotation state of turntable

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
    api_instance = DeviceServer.DevicesApi(api_client)
    device_id = 'device_id_example' # str | 
target_angle = 56 # int | Target Angle

    try:
        # PUT Rotation
        api_instance.put_device_rotation_angle(device_id, target_angle)
    except ApiException as e:
        print("Exception when calling DevicesApi->put_device_rotation_angle: %s\n" % e)
```

### Parameters

Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **device_id** | **str**|  | 
 **target_angle** | **int**| Target Angle | 

### Return type

void (empty response body)

### Authorization

No authorization required

### HTTP request headers

 - **Content-Type**: Not defined
 - **Accept**: Not defined

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

# **put_device_rotation_angle_continuous**
> put_device_rotation_angle_continuous(device_id, target_angle, direction=direction)

PUT Continious Rotation

Put continious rotation angle for device

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
    api_instance = DeviceServer.DevicesApi(api_client)
    device_id = 'device_id_example' # str | 
target_angle = 56 # int | Target Angle
direction = 56 # int | Direction of rotation (optional)

    try:
        # PUT Continious Rotation
        api_instance.put_device_rotation_angle_continuous(device_id, target_angle, direction=direction)
    except ApiException as e:
        print("Exception when calling DevicesApi->put_device_rotation_angle_continuous: %s\n" % e)
```

### Parameters

Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **device_id** | **str**|  | 
 **target_angle** | **int**| Target Angle | 
 **direction** | **int**| Direction of rotation | [optional] 

### Return type

void (empty response body)

### Authorization

No authorization required

### HTTP request headers

 - **Content-Type**: Not defined
 - **Accept**: Not defined

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

# **put_device_rotation_speed**
> put_device_rotation_speed(device_id, speed)

PUT Turntable Speed

Put the turntable speed.

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
    api_instance = DeviceServer.DevicesApi(api_client)
    device_id = 'device_id_example' # str | 
speed = 3.4 # float | Desired Speed

    try:
        # PUT Turntable Speed
        api_instance.put_device_rotation_speed(device_id, speed)
    except ApiException as e:
        print("Exception when calling DevicesApi->put_device_rotation_speed: %s\n" % e)
```

### Parameters

Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **device_id** | **str**|  | 
 **speed** | **float**| Desired Speed | 

### Return type

void (empty response body)

### Authorization

No authorization required

### HTTP request headers

 - **Content-Type**: Not defined
 - **Accept**: Not defined

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

# **put_devices_led_index**
> put_devices_led_index(device_id, led_index, state)

PUT state of LED

Set led at index on selected device

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
    api_instance = DeviceServer.DevicesApi(api_client)
    device_id = 'device_id_example' # str | UUID of device
led_index = 56 # int | Index of LED
state = True # bool | True = LED on, False = LED off

    try:
        # PUT state of LED
        api_instance.put_devices_led_index(device_id, led_index, state)
    except ApiException as e:
        print("Exception when calling DevicesApi->put_devices_led_index: %s\n" % e)
```

### Parameters

Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **device_id** | **str**| UUID of device | 
 **led_index** | **int**| Index of LED | 
 **state** | **bool**| True &#x3D; LED on, False &#x3D; LED off | 

### Return type

void (empty response body)

### Authorization

No authorization required

### HTTP request headers

 - **Content-Type**: Not defined
 - **Accept**: Not defined

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

# **put_devices_ports**
> put_devices_ports(device_id, port_index, state)

PUT state of port

Set state of port. 

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
    api_instance = DeviceServer.DevicesApi(api_client)
    device_id = 'device_id_example' # str | UUID of device
port_index = 56 # int | Index of port
state = 56 # int | state id to switch to, 1 or more

    try:
        # PUT state of port
        api_instance.put_devices_ports(device_id, port_index, state)
    except ApiException as e:
        print("Exception when calling DevicesApi->put_devices_ports: %s\n" % e)
```

### Parameters

Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **device_id** | **str**| UUID of device | 
 **port_index** | **int**| Index of port | 
 **state** | **int**| state id to switch to, 1 or more | 

### Return type

void (empty response body)

### Authorization

No authorization required

### HTTP request headers

 - **Content-Type**: Not defined
 - **Accept**: Not defined

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

# **put_halt_rotation**
> put_halt_rotation(device_id)

PUT Halt Rotation

Stop the rotation of the turntable.

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
    api_instance = DeviceServer.DevicesApi(api_client)
    device_id = 'device_id_example' # str | 

    try:
        # PUT Halt Rotation
        api_instance.put_halt_rotation(device_id)
    except ApiException as e:
        print("Exception when calling DevicesApi->put_halt_rotation: %s\n" % e)
```

### Parameters

Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **device_id** | **str**|  | 

### Return type

void (empty response body)

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
**404** | Not Found |  -  |
**500** | Internal Server Error |  -  |

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

# **put_port_led_state**
> put_port_led_state(device_id, port_index, led_index, state)

PUT state of Port LED

Set led at index on specified device's port

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
    api_instance = DeviceServer.DevicesApi(api_client)
    device_id = 'device_id_example' # str | UUID of device
port_index = 56 # int | Index of Port
led_index = 56 # int | Index of Led
state = True # bool | True = LED on, False = LED off

    try:
        # PUT state of Port LED
        api_instance.put_port_led_state(device_id, port_index, led_index, state)
    except ApiException as e:
        print("Exception when calling DevicesApi->put_port_led_state: %s\n" % e)
```

### Parameters

Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **device_id** | **str**| UUID of device | 
 **port_index** | **int**| Index of Port | 
 **led_index** | **int**| Index of Led | 
 **state** | **bool**| True &#x3D; LED on, False &#x3D; LED off | 

### Return type

void (empty response body)

### Authorization

No authorization required

### HTTP request headers

 - **Content-Type**: Not defined
 - **Accept**: Not defined

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

# **put_port_port_id_label**
> put_port_port_id_label(port_id, label=label)

PUT the label for a Port

set the label for the port identified by the given id

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
    api_instance = DeviceServer.DevicesApi(api_client)
    port_id = 'port_id_example' # str | id of port for which label applies
label = 'label_example' # str | new label for the given port (optional)

    try:
        # PUT the label for a Port
        api_instance.put_port_port_id_label(port_id, label=label)
    except ApiException as e:
        print("Exception when calling DevicesApi->put_port_port_id_label: %s\n" % e)
```

### Parameters

Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **port_id** | **str**| id of port for which label applies | 
 **label** | **str**| new label for the given port | [optional] 

### Return type

void (empty response body)

### Authorization

No authorization required

### HTTP request headers

 - **Content-Type**: Not defined
 - **Accept**: Not defined

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

# **put_port_port_id_state_label**
> put_port_port_id_state_label(port_id, state_label=state_label)

PUT state label

set the state label for the port identified by the given id

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
    api_instance = DeviceServer.DevicesApi(api_client)
    port_id = 'port_id_example' # str | id of port for which state label applies
state_label = 'state_label_example' # str | new state label for the given port (optional)

    try:
        # PUT state label
        api_instance.put_port_port_id_state_label(port_id, state_label=state_label)
    except ApiException as e:
        print("Exception when calling DevicesApi->put_port_port_id_state_label: %s\n" % e)
```

### Parameters

Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **port_id** | **str**| id of port for which state label applies | 
 **state_label** | **str**| new state label for the given port | [optional] 

### Return type

void (empty response body)

### Authorization

No authorization required

### HTTP request headers

 - **Content-Type**: Not defined
 - **Accept**: Not defined

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

# **put_port_states_port_id**
> put_port_states_port_id(port_id, port_state=port_state)



Updates the list of port states for given port 

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
    api_instance = DeviceServer.DevicesApi(api_client)
    port_id = 'port_id_example' # str | 
port_state = [DeviceServer.PortState()] # list[PortState] | Array of ports states to be used for the port given (optional)

    try:
        # 
        api_instance.put_port_states_port_id(port_id, port_state=port_state)
    except ApiException as e:
        print("Exception when calling DevicesApi->put_port_states_port_id: %s\n" % e)
```

### Parameters

Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **port_id** | **str**|  | 
 **port_state** | [**list[PortState]**](PortState.md)| Array of ports states to be used for the port given | [optional] 

### Return type

void (empty response body)

### Authorization

No authorization required

### HTTP request headers

 - **Content-Type**: application/json
 - **Accept**: Not defined

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

# **put_ports_pulse**
> put_ports_pulse(device_id, port_index, time, state)

PUT port into state for period of time

Pulse port from one state to another for a period of time in seconds

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
    api_instance = DeviceServer.DevicesApi(api_client)
    device_id = 'device_id_example' # str | UUID of device
port_index = 56 # int | Index of port
time = 3.4 # float | time in seconds to press for 0.1 = 100ms
state = 56 # int | state to switch to

    try:
        # PUT port into state for period of time
        api_instance.put_ports_pulse(device_id, port_index, time, state)
    except ApiException as e:
        print("Exception when calling DevicesApi->put_ports_pulse: %s\n" % e)
```

### Parameters

Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **device_id** | **str**| UUID of device | 
 **port_index** | **int**| Index of port | 
 **time** | **float**| time in seconds to press for 0.1 &#x3D; 100ms | 
 **state** | **int**| state to switch to | 

### Return type

void (empty response body)

### Authorization

No authorization required

### HTTP request headers

 - **Content-Type**: Not defined
 - **Accept**: Not defined

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

# **put_relay_state**
> put_relay_state(device_id, index, state)



Put state of relay at index

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
    api_instance = DeviceServer.DevicesApi(api_client)
    device_id = 'device_id_example' # str | 
index = 56 # int | index of relay to set state
state = True # bool | state to put

    try:
        # 
        api_instance.put_relay_state(device_id, index, state)
    except ApiException as e:
        print("Exception when calling DevicesApi->put_relay_state: %s\n" % e)
```

### Parameters

Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **device_id** | **str**|  | 
 **index** | **int**| index of relay to set state | 
 **state** | **bool**| state to put | 

### Return type

void (empty response body)

### Authorization

No authorization required

### HTTP request headers

 - **Content-Type**: Not defined
 - **Accept**: Not defined

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

# **put_serial_test_message**
> put_serial_test_message(device_id, port_index, serial_message)

Serial Message Test

Send a serial message to the device SerialUSB bus

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
    api_instance = DeviceServer.DevicesApi(api_client)
    device_id = 'device_id_example' # str | Device ID
port_index = 3.4 # float | Port Index
serial_message = 'serial_message_example' # str | Serial message to SerialUSB

    try:
        # Serial Message Test
        api_instance.put_serial_test_message(device_id, port_index, serial_message)
    except ApiException as e:
        print("Exception when calling DevicesApi->put_serial_test_message: %s\n" % e)
```

### Parameters

Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **device_id** | **str**| Device ID | 
 **port_index** | **float**| Port Index | 
 **serial_message** | **str**| Serial message to SerialUSB | 

### Return type

void (empty response body)

### Authorization

No authorization required

### HTTP request headers

 - **Content-Type**: Not defined
 - **Accept**: Not defined

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

# **put_state_by_port_id**
> put_state_by_port_id(port_id, state)

PUT state of port

Set State of Port by id 

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
    api_instance = DeviceServer.DevicesApi(api_client)
    port_id = 'port_id_example' # str | id of port to set
state = 56 # int | state id to switch to, 1 or more

    try:
        # PUT state of port
        api_instance.put_state_by_port_id(port_id, state)
    except ApiException as e:
        print("Exception when calling DevicesApi->put_state_by_port_id: %s\n" % e)
```

### Parameters

Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **port_id** | **str**| id of port to set | 
 **state** | **int**| state id to switch to, 1 or more | 

### Return type

void (empty response body)

### Authorization

No authorization required

### HTTP request headers

 - **Content-Type**: Not defined
 - **Accept**: Not defined

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

