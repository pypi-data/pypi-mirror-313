# Migrating `faraday.inria.fr`


## Historical Notes

### Initial plan

The general angle for setting up R2lab initially was to mostly mimick NITOS. That is why we run NITOS nodes in the first place.

As part of that plan, the first installation of `faraday.inria.fr` was based on Ubuntu, as it was a requirement for installing OMF.

### Mid-term

After some time we decided that OMF was not the right choice for us, so I came
up with a rather different story, with
* `rhubarbe` running on `faraday.inria.fr` for close-contact node management,
* and a MyPLC instance on `r2labapi.inria.fr` for managing accounts and leases - and ideally federation - instead of the OMF junk.

### 2019

Then there was the realization that `faraday.inria.fr` was the only single box
running Ubuntu in the whole datacenter overhere at Inria Sophia, and that there
was no good reason for that choice since OMF is long gone.

So I decided to rebuild the box entirely, and to this end I am writing down these notes, that ideally will shed light on how the whole thing actually works.

## Status before migration

```
root@faraday ~ (master) # cat /etc/lsb-release
DISTRIB_ID=Ubuntu
DISTRIB_RELEASE=16.04
DISTRIB_CODENAME=xenial
DISTRIB_DESCRIPTION="Ubuntu 16.04.5 LTS"
```

```
root@faraday ~ (master) # pip3 freeze | grep rhubarbe
rhubarbe==2.0.2
```

### Storage

* There's a total of 6.5 Tb on the box; no problem here.
* However when rebuilding we'll need to backup something in the 1.2Tb; sufficient space is available in `bigjohn:/vservers/backup/faraday`
  * /var/lib/rhubarbe-images
  * /home
  * /etc
  * /root
  * **and probably more**

Current partitioning is based on LVM, which is quite wrong. When rebuilding it would make a lot of sense to

### Fixed User

There is one user named `faraday` that is created manually.

```
root@faraday ~ (master) # grep faraday /etc/passwd
faraday:x:1003:1003::/home/faraday:
```
```
root@faraday ~ (master) # ls -ld /home/faraday
drwxr-xr-x 6 faraday faraday 4096 Dec 12 11:37 /home/faraday
```

Nothing much in there, and no access from the outside:

```
root@faraday ~ (master) # ls -l /home/faraday
total 8
drwxrwxr-x  9 faraday faraday 4096 Dec 12 11:15 diana
drwxrwxr-x 13 faraday faraday 4096 Dec 12 11:29 r2lab-embedded
```
```
root@faraday ~ (master) # ls -la /home/faraday/.ssh
total 8
drwx------ 2 faraday faraday 4096 Jun 16  2015 .
drwxr-xr-x 6 faraday faraday 4096 Dec 12 11:37 ..
```

The general idea was only for root to be able to publish material readable from
real slice users. Come to think about it, it was maybe not the best choice, as
this area sometimes requires miscellaneous contorsions when it comes to updating
it.

### Digression on bash profiles

As an example, the commonly accessible bash profiles (typically `faraday.sh`) are exposed to regular users as hooks in `/etc/profile.d`, like this:

```
root@faraday /etc/profile.d (master) # ls -l /etc/profile.d/
total 12
-rw-r--r-- 1 root root  663 Apr  7  2014 bash_completion.sh
-rw-r--r-- 1 root root 1003 Dec 29  2015 cedilla-portuguese.sh
lrwxrwxrwx 1 root root   45 Jan 31  2018 faraday.sh -> /home/faraday/r2lab-embedded/shell/faraday.sh
lrwxrwxrwx 1 root root   48 Jan 31  2018 r2labutils.sh -> /home/faraday/r2lab-embedded/shell/r2labutils.sh
-rw-r--r-- 1 root root 1557 Apr 14  2016 Z97-byobu.sh
```

### User account management

User accounts get synced to mirror the set of active slices in the
`r2labapi.inria.fr` website; this is done by the following service, which is part of rhubarbe.

```
root@faraday /etc/profile.d (master) # systemctl status accountsmanager
● accountsmanager.service - testbed accounts manager - manages unix accounts and their authorized_keys
   Loaded: loaded (/etc/systemd/system/accountsmanager.service; enabled; vendor preset: enabled)
   Active: active (running) since Tue 2019-01-08 06:00:05 CET; 4h 54min ago
 Main PID: 18929 (rhubarbe-accoun)
   CGroup: /system.slice/accountsmanager.service
           └─18929 /usr/bin/python3 /usr/local/bin/rhubarbe-accounts

Jan 08 06:00:05 faraday systemd[1]: Started testbed accounts manager - manages unix accounts and their authorized_keys.
```

### Images

```
root@faraday ~ (master) # du -hs /var/lib/rhubarbe-images/
340G	/var/lib/rhubarbe-images/
```
Out of which 100 Gb are probably not useful:
```
root@faraday ~ (master) # du -hs /var/lib/rhubarbe-images/archive*
12G	/var/lib/rhubarbe-images/archive
85G	/var/lib/rhubarbe-images/archive-oai
```

### Miscell

* using `diana` bash components : `gitprompt git miscell systemd` and `BASH_BANNER_STYLE="5"`
* remember to reinstall `megacli` for RAID monitoring, as well as the backup/rsync-sender thingy
* root crontab is saved in `/root/.crontab-faraday`


## The plan

* backup - see `/root/backup.sh`
  * `/home /var/lib/rhubarbe-images /root /etc /tftpboot`
  * goes on `bigjohn:/vservers/backup/faraday`
* tear down faraday, reinstall fedora
  * partitioning: /boot + / : **both as ext4**
  * turn off ssh pasword authentication, restore keys, enable remote access
  * redo udev and network configuration - see [[faraday-network]]

* pour backup into `/incoming`

* reboot and use remote access
  * reinstall inventory, set up dnsmasq
  * reinstall rhubarbe and related config
  * esp. wrt r2labapi / check rleases
  * redo port forwarding for VLC/Screen Sharing
  * turn off SELINUX that prevents dnsmasq from running properly


* restore big chuks as-is
  * user entries in `/etc/passwd`, `/home`, check ownerships if needed
  * `/var/lib/rhubarbe-images`
  * `/root`
  * `/tftpboot`

## remains todo

* ~~install megacli from semir rpms~~
* ~~check backupscope (i.e. `.rsync-filter`) on faraday~~
* check contents from `/root`
* fix rhubarbe issues on github for smoother operations

## Hard points

* partitioning based on ext4; preserved BIOS partition (?) on `/dev/sd1` - (it felt like I had to, could not get the fedora install program to accept a simpler layout)
* **disabling selinux** is needed (dnsmasq would not have worked; I take it that `/tftpboot` would have needed to be recreated with proper context)
* I went for **`NetworkManager`** to be consistent with the rest of the cloud boxes
* likewise I went for relying on **the `iptables` service** and not on firewalld
* struggled a bit to find out that **IP forwarding** is not enabled by default
