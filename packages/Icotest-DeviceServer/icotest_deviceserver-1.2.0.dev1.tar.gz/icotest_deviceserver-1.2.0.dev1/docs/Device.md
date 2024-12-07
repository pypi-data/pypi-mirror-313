# Device

Model representing a device, used for both API interactions and database storage. This model includes attributes such as device ID, index, name, type, and various counts (ports, buttons, LEDs), as well as a serial number. 

## Properties
Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**device_id** | **str** |  | 
**device_index** | **int** |  | 
**device_type** | **str** |  | [optional] 
**device_serial** | **str** |  | [optional] 
**name** | **str** |  | 
**description** | **str** |  | [optional] 
**port_count** | **int** | Number of ports available on device | [optional] 
**button_count** | **int** | Number of buttons available on device | [optional] 
**led_count** | **int** | Number of leds available on device | [optional] 
**temperature_port_count** | **int** | Number of temperature ports available on device | [optional] 

[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)


