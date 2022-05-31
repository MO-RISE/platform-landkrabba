# platform-landkrabba

A sensor platform consisting of:
- A Navico radar
- An Ouster lidar
- 4x Axis cameras
- 2x RTL-SDR receivers connected to a VHF antenna
- 1x WindObserver 65

The sensors are eventually interfaced to a [crowsnest](https://github.com/MO-RISE/crowsnest) data bus:
- Navico radar -> OpenDLV/libcluon -> crowsnest
- Ouster lidar -> crowsnest
- Axis cameras -> crowsnest
- RTL-SDR receivers -> crowsnest
- WindObserver 65 -> crowsnest

## Network setup

Connected as:
* Ethernet port 1 <-> Navico radar
* Ethernet port 2 <-> Ouster lidar
* Ethernet port 3 <-> Axis F44 hub
* Ethernet port 6 <-> 4G router (192.168.1.1)
* USB ports <-> RTL-SDRs
* USB ports <-> WindObserver 65

Configuration:

* `netplan` config in `netplan-platform-landkrabba.yaml`
    * Copy file to `/etc/netplan/`
    * Apply using `sudo netplan apply`
* Axis F44 hub assumed to be assigned the static IP `10.10.10.2`
* Ouster Lidar assumed to be assigned the static IP `10.10.20.100` (Note: For setting a static IP, refer to [this](https://forum.ouster.at/d/63-how-i-can-assign-static-ip-to-os1))

Checks:

* `ethtool enp1s0` should show connected
* `ethtool enp2s0` should show connected
* `ethtool enp3s0` should show connected
* `ping 10.10.10.2` should work
* `ip route show` should show a 236.6.7.0/24 route to enp1s0
* `ip route show` should show a 10.10.10.2 route to enp3s0
* `sudo arp-scan --interface=enp2s0 10.10.20.0/24` should output:
  ```
  10.10.20.100    <MAC address>       Ouster
  ```
* `ping 10.10.20.100` should work

  
## Live stream/logging software setup

All of the below assumes a crowsnest setup is already up and running according to [the base setup](https://github.com/MO-RISE/crowsnest/blob/main/docker-compose.base.yml).

Clone this repo to (suggestion): `/opt/platform-landkrabba` and run as follows:

Sensor interfaces:
  * Only AIS receiver: `docker-compose -f docker-compose.ais.yml up -d`
  * Only cameras: `docker-compose -f docker-compose.cameras.yml up -d`
  * Only Lidar: `docker-compose -f docker-compose.lidar.yml up -d`
  * Only Radar: `docker-compose -f docker-compose.radar.yml up -d`
  * Only Wind sensor: `docker-compose -f docker-compose.nmea0183.yml up -d`

Bridges towards Maritimeweb:
  * Only mqtt bridge: `docker-compose -f docker-compose.bridge.yml up -d`
  * Only webrtc bridge: `docker-compose -f docker-compose.webrtc.yml up -d`


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


