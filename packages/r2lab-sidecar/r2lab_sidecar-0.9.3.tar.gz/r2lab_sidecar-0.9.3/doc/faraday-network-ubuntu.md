###  `ip link sh`:

manually selected:

```
2: internet: <BROADCAST,MULTICAST,UP,LOWER_UP> mtu 1500 qdisc mq state UP mode DEFAULT group default qlen 1000
    link/ether c8:1f:66:f4:11:62 brd ff:ff:ff:ff:ff:ff
3: optical: <BROADCAST,MULTICAST,PROMISC,UP,LOWER_UP> mtu 1500 qdisc mq portid 000af75d7bf0 state UP mode DEFAULT group default qlen 1000
    link/ether 00:0a:f7:5d:7b:f0 brd ff:ff:ff:ff:ff:ff
4: em2: <BROADCAST,MULTICAST> mtu 1500 qdisc noop state DOWN mode DEFAULT group default qlen 1000
    link/ether c8:1f:66:f4:11:63 brd ff:ff:ff:ff:ff:ff
<same for em3 em4 p2p2>
8: reboot@optical: <BROADCAST,MULTICAST,UP,LOWER_UP> mtu 1500 qdisc noqueue state UP mode DEFAULT group default qlen 1000
    link/ether 00:0a:f7:5d:7b:f0 brd ff:ff:ff:ff:ff:ff
9: data@optical: <BROADCAST,MULTICAST,UP,LOWER_UP> mtu 1500 qdisc noqueue state UP mode DEFAULT group default qlen 1000
    link/ether 00:0a:f7:5d:7b:f0 brd ff:ff:ff:ff:ff:ff
10: control@optical: <BROADCAST,MULTICAST,UP,LOWER_UP> mtu 1500 qdisc noqueue state UP mode DEFAULT group default qlen 1000
    link/ether 00:0a:f7:5d:7b:f0 brd ff:ff:ff:ff:ff:ff
11: switches@optical: <BROADCAST,MULTICAST,UP,LOWER_UP> mtu 1500 qdisc noqueue state UP mode DEFAULT group default qlen 1000
    link/ether 00:0a:f7:5d:7b:f0 brd ff:ff:ff:ff:ff:ff
```

### `ip address show`

ditto:

```
2: internet: <BROADCAST,MULTICAST,UP,LOWER_UP> mtu 1500 qdisc mq state UP group default qlen 1000
    link/ether c8:1f:66:f4:11:62 brd ff:ff:ff:ff:ff:ff
    inet 138.96.16.97/28 brd 138.96.16.111 scope global internet
       valid_lft forever preferred_lft forever
    inet 138.96.16.99/28 scope global secondary internet
       valid_lft forever preferred_lft forever
    inet 138.96.16.100/28 scope global secondary internet
       valid_lft forever preferred_lft forever
    inet 138.96.16.101/28 scope global secondary internet
       valid_lft forever preferred_lft forever
    inet 138.96.16.102/28 scope global secondary internet
       valid_lft forever preferred_lft forever
    inet6 fe80::ca1f:66ff:fef4:1162/64 scope link
       valid_lft forever preferred_lft forever
3: optical: <BROADCAST,MULTICAST,PROMISC,UP,LOWER_UP> mtu 1500 qdisc mq portid 000af75d7bf0 state UP group default qlen 1000
    link/ether 00:0a:f7:5d:7b:f0 brd ff:ff:ff:ff:ff:ff
    inet 192.168.0.100/24 brd 192.168.0.255 scope global optical
       valid_lft forever preferred_lft forever
    inet6 fe80::20a:f7ff:fe5d:7bf0/64 scope link
       valid_lft forever preferred_lft forever
8: reboot@optical: <BROADCAST,MULTICAST,UP,LOWER_UP> mtu 1500 qdisc noqueue state UP group default qlen 1000
    link/ether 00:0a:f7:5d:7b:f0 brd ff:ff:ff:ff:ff:ff
    inet 192.168.1.100/24 brd 192.168.1.255 scope global reboot
       valid_lft forever preferred_lft forever
    inet6 fe80::20a:f7ff:fe5d:7bf0/64 scope link
       valid_lft forever preferred_lft forever
9: data@optical: <BROADCAST,MULTICAST,UP,LOWER_UP> mtu 1500 qdisc noqueue state UP group default qlen 1000
    link/ether 00:0a:f7:5d:7b:f0 brd ff:ff:ff:ff:ff:ff
    inet 192.168.2.100/24 brd 192.168.2.255 scope global data
       valid_lft forever preferred_lft forever
    inet6 fe80::20a:f7ff:fe5d:7bf0/64 scope link
       valid_lft forever preferred_lft forever
10: control@optical: <BROADCAST,MULTICAST,UP,LOWER_UP> mtu 1500 qdisc noqueue state UP group default qlen 1000
    link/ether 00:0a:f7:5d:7b:f0 brd ff:ff:ff:ff:ff:ff
    inet 192.168.3.100/24 brd 192.168.1.255 scope global control
       valid_lft forever preferred_lft forever
    inet6 fe80::20a:f7ff:fe5d:7bf0/64 scope link
       valid_lft forever preferred_lft forever
11: switches@optical: <BROADCAST,MULTICAST,UP,LOWER_UP> mtu 1500 qdisc noqueue state UP group default qlen 1000
    link/ether 00:0a:f7:5d:7b:f0 brd ff:ff:ff:ff:ff:ff
    inet 192.168.4.100/24 brd 192.168.4.255 scope global switches
       valid_lft forever preferred_lft forever
    inet6 fe80::20a:f7ff:fe5d:7bf0/64 scope link
       valid_lft forever preferred_lft forever
```

### ubuntu interfaces

```
root@faraday /etc/network (master) # cat interfaces
# This file describes the network interfaces available on your system
# and how to activate them. For more information, see interfaces(5).

# see also /etc/udev/rules.d/80-net-setup-link.rules
# for naming the internet and optical interfaces

# The loopback network interface
auto lo
iface lo inet loopback

# The primary network interface
auto internet
  iface internet inet static
  address 138.96.16.97
  netmask 255.255.255.240
  gateway 138.96.16.110
  dns-search inria.fr
  dns-nameservers 138.96.0.10 138.96.0.11
  # fraday-macphone1 and others
  up ip address add 138.96.16.99/28  dev internet
  up ip address add 138.96.16.100/28 dev internet
  up ip address add 138.96.16.101/28 dev internet
  up ip address add 138.96.16.102/28 dev internet

### the optical interface
# its main IP is on the 192.168.4.0/24 subnet
# which is together with the 4 Dell switches
# we now define following VLANs on this interface
# 10 : reboot
# 20 : data
# 30 : control
# 40 : switches
# NOTE:
# in a former setup it was important to have
# .3.100 *mentioned first* because the first address
# is the one used as the source address
# in DHCPOFFER packets sent by the DHCP server
# and apparently the BIOS network boot agent on our nodes
# expects this to be identical to the IP address offered
# NOTE:
# as an extra goody optical is set in promisc mode
auto optical
  iface optical inet static
    # this IP address is not used, traffic would be untagged
    address 192.168.0.100
    netmask 255.255.255.0
    ########## up
    # promisc
    up ip link set $IFACE promisc on
    # virtual interface 'reboot' on vlan 10 and subnet 192.168.1.x
    up ip link add link optical name reboot type vlan id 10
    up ip link set dev reboot up
    up ip addr add dev reboot 192.168.1.100/24 brd 192.168.1.255
    # virtual interface 'data' on vlan 20 and subnet 192.168.2.x
    up ip link add link optical name data type vlan id 20
    up ip link set dev data up
    up ip addr add dev data 192.168.2.100/24 brd 192.168.2.255
    # virtual interface 'control' on vlan 30 and subnet 192.168.3.x
    up ip link add link optical name control type vlan id 30
    up ip link set dev control up
    up ip addr add dev control 192.168.3.100/24 brd 192.168.1.255
    # virtual interface 'switches' on vlan 40 and subnet 192.168.4.x
    up ip link add link optical name switches type vlan id 40
    up ip link set dev switches up
    up ip addr add dev switches 192.168.4.100/24 brd 192.168.4.255
    ########## down
    down ip link delete dev reboot
    down ip link delete dev data
    down ip link delete dev control
    down ip link delete dev switches
    # promisc
    down ip link set $IFACE promisc off

# limit multicast traffic to the control network for now
up ip route add 224.0.0.0/4 dev control
```
