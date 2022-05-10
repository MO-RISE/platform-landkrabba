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


# NOTE: Below is not up-to-date!
  
## Logging software setup

* Clone this repo
* Run logging as:
    * Only cameras: `docker-compose -f docker-compose.cameras.yml up -d`
    * Only Navico: `docker-compose -f docker-compose.navico.yml up -d`
    * Only ARS-300: `docker-compose -f docker-compose.ars300.yml up -d`
    * All: `docker-compose -f docker-compose.cameras.yml -f docker-compose.navico.yml -f docker-compose.ars300.yml up -d`

By default, all data will be put in `/media/sealog/platform_landkrabba/`

The data being logged are stored in odvd-format (radars) and mp4v-format (cameras). mp4v can be played directly by for example [VLC](https://www.videolan.org/). In order to read the *.rec-files with radar data and odvd-specification is needed.

ODVD main spec: `https://github.com/MO-RISE/memo/tree/v0.3.1`
Extra ODVD spec for Navico radar:
```
message opendlv.proxy.RadarDetectionReading [id = 1201] {
  float azimuth [id = 1];
  bytes data [id = 2]; // RawData
  float range [id = 3];
}
```

Can be used together with `cluon-rec2csv` to extract data in csv-format. `cluon-rec2csv` can (for example) be installed trough [pycluon](https://github.com/MO-RISE/pycluon), i.e. `pip install pycluon`



## Hardware setup

Current location: REVERE Labet 
In use for REEDs project 

Base architecture 
- Power system 
   - 12V 
   - Battery 75ah 
   - Battery charger (230V)
   - Switchboard with Cylinder fuse 6x32mm (6 switches)
- weatherproof box for electrical system and compute units 
- Battery installed in weatherproof box
- Charger installed in weatherproof box

![image](https://user-images.githubusercontent.com/36690474/145045628-fd7898c7-4946-43c4-b808-15ec29450f91.png)

[Draw.io image source](https://risecloud-my.sharepoint.com/:u:/g/personal/ted_sjoblom_ri_se/EY4vCbqoZQ5EkSwt1cZGcOkBLVDilikyGcOJKVD8jE3cgA?e=7hvwcj) 

![image](photos/20211221_083533.jpg)
![image](photos/20211221_083604.jpg)
![image](photos/20211221_114753.jpg)
![Untitled picture](https://user-images.githubusercontent.com/36690474/149301345-a61ca7d6-5868-4c8b-ada7-d0dabbe5560b.png)
