### udev

```
root@faraday /etc/udev/rules.d (master) # cat /etc/udev/rules.d/80-net-setup-link.rules
# This machine is most likely a virtualized guest, where the old persistent
# network interface mechanism (75-persistent-net-generator.rules) did not work.
# This file disables /lib/udev/rules.d/80-net-setup-link.rules to avoid
# changing network interface names on upgrade. Please read
# /usr/share/doc/udev/README.Debian.gz about how to migrate to the currently
# supported mechanism.
#
# as per ip add show
# em1 =     c8:1f:66:f4:11:62
# as per lspci
# 01:00.0 = c8-1f-66-f4-11-62
# rename em1 as internet
SUBSYSTEM=="net", ACTION=="add", KERNELS=="0000:01:00.0", NAME="internet"
# as per ip add show
# p2p1 = 00:0a:f7:5d:7b:f0
# as per lspci
# 44:00.0 = 00-0a-f7-ff-fe-5d-7b-f0
SUBSYSTEM=="net", ACTION=="add", KERNELS=="0000:44:00.0", NAME="optical"
```

### network per se

See local directory `./network-scripts/` for a first stab at reproducing the ubuntu network config that is captured in more details in [[faraday-network-ubuntu]]

### port forwarding

VNC sessions to the macphone(s) are based on
* multiple IP addresses attached to the 'internet' interface
* port 5900 forwarded to the individual macphones through iptables:
* we have 5 rules, for compat the main IP address for faraday is redirected to macphone1 (sohuld probably drop that behaviour)

```
/etc/iptables/rules.v4:-A PREROUTING -d  138.96.16.97/32 -p tcp -m tcp --dport 5900 -j DNAT --to-destination 192.168.4.201:5900
/etc/iptables/rules.v4:-A PREROUTING -d  138.96.16.99/32 -p tcp -m tcp --dport 5900 -j DNAT --to-destination 192.168.4.201:5900
/etc/iptables/rules.v4:-A PREROUTING -d 138.96.16.100/32 -p tcp -m tcp --dport 5900 -j DNAT --to-destination 192.168.4.202:5900
/etc/iptables/rules.v4:-A PREROUTING -d 138.96.16.101/32 -p tcp -m tcp --dport 5900 -j DNAT --to-destination 192.168.4.203:5900
/etc/iptables/rules.v4:-A PREROUTING -d 138.96.16.102/32 -p tcp -m tcp --dport 5900 -j DNAT --to-destination 192.168.4.204:5900
```

### inventory / dnsmasq

Remember we have a tool in `r2lab-misc/inventory/configure.py`
that helps populating files like `/etc/hosts` and `dnsmasq` config
