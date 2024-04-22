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
