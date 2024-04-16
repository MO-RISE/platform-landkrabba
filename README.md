# platform-landkrabba

A sensor platform consisting of:

- 1x Navico radar 24
- 1x Ouster lidar (OS2)
- 1x AXIS camera (P1375-E)

The sensors are interfaced to a [crowsnest](https://github.com/MO-RISE/crowsnest) data bus:

- Navico radar -> OpenDLV/libcluon -> crowsnest
- Ouster lidar -> crowsnest
- Axis cameras -> crowsnest

## Network setup

Connected as:

- Ethernet port 1 <-> Navico radar 25
- Ethernet port 2 <-> Ouster lidar (OS2)
- Ethernet port 3 <-> AXIS camera (10.10.70.2)
- Ethernet port 6 <-> 4G router (192.168.1.1)
- USB ports <-> NA
- USB ports <-> NA

**Checks:**

- `ethtool enp1s0` should show --> Link detected: yes
- `ethtool enp2s0` should show --> Link detected: yes
- `ethtool enp3s0` should show --> Link detected: yes
- `ping 10.10.10.2` should work
- `ip route show` should show a 236.6.7.0/24 route to enp1s0
- `ip route show` should show a 10.10.10.2 route to enp3s0
- `sudo arp-scan --interface=enp2s0 10.10.20.0/24` should output:
  ```
  10.10.20.100    <MAC address>       Ouster
  ```
- `ping 10.10.20.100` should work

**Configuration:**

- `netplan` config in `netplan-platform-landkrabba.yaml`
  - Copy file to `/etc/netplan/`
  - Apply using `sudo netplan apply`
- Axis F44 hub assumed to be assigned the static IP `10.10.10.2`
- Ouster Lidar assumed to be assigned the static IP `10.10.20.100` (Note: For setting a static IP, refer to [this](https://forum.ouster.at/d/63-how-i-can-assign-static-ip-to-os1))


### Configuring Ouster hardware

Using the [TCP API](https://static.ouster.dev/sensor-docs/image_route1/image_route2/common_sections/API/tcp-api.html):

```
nc 10.10.20.100 7501
set_config_param <param_name> <value>
.
.
.
reinit
save_config_params
```

The final configuration of the sensor for this setup is as follows:

```json
{
  "udp_ip": "10.10.20.1",
  "udp_dest": "10.10.20.1",
  "udp_port_lidar": 7502,
  "udp_port_imu": 7503,
  "timestamp_mode": "TIME_FROM_INTERNAL_OSC",
  "sync_pulse_in_polarity": "ACTIVE_HIGH",
  "nmea_in_polarity": "ACTIVE_HIGH",
  "nmea_ignore_valid_char": 0,
  "nmea_baud_rate": "BAUD_9600",
  "nmea_leap_seconds": 0,
  "multipurpose_io_mode": "OFF",
  "sync_pulse_out_polarity": "ACTIVE_HIGH",
  "sync_pulse_out_frequency": 1,
  "sync_pulse_out_angle": 360,
  "sync_pulse_out_pulse_width": 10,
  "auto_start_flag": 1,
  "operating_mode": "NORMAL",
  "lidar_mode": "512x10",
  "azimuth_window": [0, 360000],
  "signal_multiplier": 1,
  "phase_lock_enable": false,
  "phase_lock_offset": 0
}
```

Note that the Ouster SDK does not yet support multicast (https://github.com/ouster-lidar/ouster_example/pull/278) and as such only a single microservice may interface with the Ouster at any given time. As such, only one of the two microservices defined in `docker-compose.lidar.yml` can be active at any given time depending on the use case.

### TODO (if time allows):

- Set up PTP according to https://static.ouster.dev/sensor-docs/image_route1/image_route2/appendix/ptp-quickstart.html#linux-ptp-grandmaster-clock


## Live stream/logging software setup

All of the below assumes a crowsnest setup is already up and running according to [the base setup](https://github.com/MO-RISE/crowsnest/blob/main/docker-compose.base.yml).

Clone this repo to (suggestion): `/opt/platform-landkrabba` and run as follows:

Sensor interfaces:

- Only Lidar: `docker-compose -f docker-compose.lidar.yml up -d`
- Only AIS receiver: `docker-compose -f docker-compose.ais.yml up -d`
- Only cameras: `docker-compose -f docker-compose.cameras.yml up -d`
- Only Radar: `docker-compose -f docker-compose.radar.yml up -d`
- Only Wind sensor: `docker-compose -f docker-compose.nmea0183.yml up -d`

Bridges towards Maritimeweb:

- Only mqtt bridge: `docker-compose -f docker-compose.bridge.yml up -d`
- Only webrtc bridge: `docker-compose -f docker-compose.webrtc.yml up -d`

To handle multiple services simultaneously, use the following syntax:

```
docker-compose -f docker-compose.<any>.yml -f docker-compose.<any>.yml -f docker-compose.<any>.yml up -d
```

Logging to disk (using opendlv):

```
docker-compose -f docker-compose.logging.yml up -d
```

The logs are rotated using logrotate according to the config found in [logrotate.conf](./logrotate.conf). By default, all data will be put in `/opt/recordings/`. This is **NOT** recommended since it may fill the OS disk. If you plan on continously log.

## To run bandwidth trials

The [`iftop`](https://linux.die.net/man/8/iftop) utility has been used to run some rudimentary bandwidth trials for the connected sensors, such as:

```bash
sudo iftop -i <interface> # Interactive output

or

sudo iftop -t -s 60 -i <interface>  # Running for 60 seconds and then outputting textual output only
```

**Note:** The above should be issued with the sensors running!

4G connection bandwidth has been trialed with [`speedtest-cli`](https://www.speedtest.net/apps/cli), such as:

```bash
speedtest-cli
```

## Radar settings

- --cid: CID of the OD4Session to send and receive messages 
- --ip: Initial reporting address of the Navico device (Typically 236.6.7.5)
-  --port: Initial Navico Broadcast Port (Typically 6878)
-  --antenna_height: Height of the sensor above the waterline (in millimetres)
-  --bearing_alignment: Unit offset from the centreline of the vehicle (in milliradians). Negative == Left)
-  --gain: Set unit Gain (in percentage. Empty is Auto)
-  --interface_rejection: 
-  --local_interface rejection:
-  --noise_rejection:
-  --transmit_lock: This  needs to be set to '0' to enable transmission
-  --rain_clutter: (in percentage. Empty is Auto)
-  --range_alpha: Set unit A Range (in metres. 50 to 72700)
-  --range_bravo: Set unit B Range (in metres. 50 to 72700)
-  --scan_speed. (1,2,3. 3 is fastest) The Halo20+ should have a huge range of scan speeds, but this is only what RadarPi uses. Scan speed 3 is 60rpm, and is only accurate to about 2.5km, according to the manual
-  --sea_clutter: (in percentage. Empty is Auto)
-  --side_lobe_suppression: CONSULT KRISTER ;) BEFORE CHANGING
-  --target_boost: (1,2,3. 3 is highest)
-  --target_expansion: (1,2,3. 3 is highest)
-  --target_seperation: (1,2,3. 3 is highest))
-  --doppler: (3 modes for target tracking. Consult ReadMe)
-  --id: ID to use for sending radar spokes"
-  --verbose: Enable more text output"
-  --raw: Enables raw data stream to terminal.
