# HOW TO GUIDE



## New platform setup

### Time syncing & (Local time or UTC?)

#### NTP 

**We using CHRONY**

The NTP daemon chronyd calculates the drift and offset of your system clock and continuously adjusts it, so there are no large corrections that could lead to inconsistent logs, for instance. The cost is a little processing power and memory, but for a modern server this is usually negligible.

Based on: <https://ubuntu.com/server/docs/network-ntp>

1. Install chrony  ``sudo apt install chrony``
2. Modify ``/etc/chrony/chrony.conf`` and add a line with a server from RISE, see here:  https://www.netnod.se/swedish-distributed-time-service
   1. Recommended:
      1. Remove all pre-configured

          ```txt
          # See http://www.pool.ntp.org/join.html for more information.
          pool 0.ubuntu.pool.ntp.org iburst maxsources 1
          pool 1.ubuntu.pool.ntp.org iburst maxsources 1
          pool 2.ubuntu.pool.ntp.org iburst maxsources 2
          ```

      2. Change to
  
          ```bash
          pool ntp.se iburst maxsources 4
          ```

3. Restart chrony using ``sudo systemctl restart chrony.service``
4. Check NTP
   1. Check NTP status
  
    ```bach
    chronyc sources

    # MS Name/IP address  Stratum Poll Reach LastRx Last sample
    # =======================================================
    # ^* ntp.netnod.se     1   7  377   24  +33us[+48us] +/-1193us
    # What is acceptable values?

    Sample under 10 000us +/-1193us
    ```

   2. Quick check for non chrony install 

   ```bash
   timedatectl status

    # Check that output is:
    #     System clock synchronized: yes
    #     NTP service: active

   ```


### Netplan Configuration:

- `netplan` config in `netplan-platform-landkrabba.yaml`
  - Copy file to `/etc/netplan/`
  - Apply using `sudo netplan apply`
- Axis F44 hub assumed to be assigned the static IP `10.10.10.2`
- Ouster Lidar assumed to be assigned the static IP `10.10.20.100` (Note: For setting a static IP, refer to [this](https://forum.ouster.at/d/63-how-i-can-assign-static-ip-to-os1))


### Configure RUTX12 Router 

1) Set IP address 10.10.10.2
2) Add static lease
   1) Set Sealog mac to and ip 10.10.10.253  
   2) Enable NMEA Server messages under GPS
      1) 10.10.10.253 port 8888 UDP


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