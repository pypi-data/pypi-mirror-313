# SonnenCharger

## Purpose

Read status information from a SonnenCharger type wallbox

## Installation

### Using `pip`

``` bash
pip3 install sonnencharger
```

### Manual installation
[Download the archive from pypi.org](https://pypi.org/project/sonnencharger/#files) and unpack where needed ;)

## Usage

``` python
from sonnencharger import sonnencharger

sc_host = '192.168.1.2'
sc_port = 502  # optional, default=502

# Init class, establish connection
sc = sonnencharger(sc_host, sc_port)

print(sc.get_sysinfo())	    # retrieve general wallbox information
print(sc.get_connectors())  # retrieve status of the connectors
```

## Results (examples)

### System information

``` python
{
  'connectors': 1,
  'hwrevision': '1.23',
  'model': 'YOUR-MODEL-ID',
  'serial': '1234567890',
  'swrevision': '1.23.45'
 }
 ```

 ### Connector Info

 ``` python
{
	0: {
		'active_session_duration': 77127,
		'active_session_imported_energy': 4.667,
		'ev_max_phase_current': 14.784,
		'ev_max_power': 0.0,
		'ev_required_energy': 0.0,
		'l1_active_power': 0.0,
		'l1_current': 0.0,
		'l1_ln_voltage': 234.4,
		'l1_phase': 1,
		'l2_active_power': 0.0,
		'l2_current': 0.0,
		'l2_ln_voltage': 233.96,
		'l2_phase': 2,
		'l3_active_power': 0.0,
		'l3_current': 0.0,
		'l3_ln_voltage': 235.34,
		'l3_phase': 3,
		'max_current': 16.0,
		'net_frequency': 49.99,
		'num_phases': 3,
		'power_factor': 0.0,
		'session_departure_time': 1673110800,
		'session_id': 0,
		'state': 'Vehicle has paused charging',
		'state_numeric': 5,
		'target_current': 16.0,
		'total_active_power': 0.0,
		'type': 'CableType2',
		'type_numeric': 2,
		'vehicle_connected_phases': 'Three phases',
		'vehicle_connected_phases_code': 0,
		'vehicle_connected_phases_numeric': 3
	}
}
```
