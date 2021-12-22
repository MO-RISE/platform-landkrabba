# platform-landkrabba

A sensor platform consisting of:
- A Navico radar
- A ARS-300 radar
- 4x Axis cameras

## Network setup

Connected as:
* Ethernet port 1 <-> Navico radar
* Ethernet port 2 <-> Axis F44 hub
* USB <-> Kvaser Leaf CAN bus

Configuration:

* `netplan` config in `netplan-platform-landkrabba.yaml`
    * Copy file to `/etc/netplan/`
    * Apply using `sudo netplan apply`
* Enable multicast on loopback interface: `sudo ifconfig lo multicast`
* Enable CAN network interface: `sudo ip link set can0 up type can bitrate 500000`
* Axis F44 hub needs to be assigned the static IP `192.168.1.100`

Checks:

* `ethtool enp1s0` should show connected
* `ethtool enp2s0` should show connected
* `ping 192.168.1.100` should work
* `ifconfig` should list a can0 interface in UP state
* `ip route show` should show a 224.0.0.0/4 route to enp1s0 (all multicast traffic via enp1s0) 

  
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

![image](https://user-images.githubusercontent.com/36690474/145045628-fd7898c7-4946-43c4-b808-15ec29450f91.png)

[Draw.io image source](https://risecloud-my.sharepoint.com/:u:/g/personal/ted_sjoblom_ri_se/EY4vCbqoZQ5EkSwt1cZGcOkBLVDilikyGcOJKVD8jE3cgA?e=7hvwcj) 


![image](photos/20211221_083533.jpg)
![image](photos/20211221_083604.jpg)
![image](photos/20211221_114753.jpg)