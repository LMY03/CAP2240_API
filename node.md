# qemu agent
sudo apt update -y

sudo apt upgrade -y

sudo apt install qemu-guest-agent -y

sudo systemctl start qemu-guest-agent

sudo ln -s /lib/systemd/system/qemu-guest-agent.service /etc/systemd/system/multi-user.target.wants/qemu-guest-agent.service

# Netdata

wget -O /tmp/netdata-kickstart.sh https://get.netdata.cloud/kickstart.sh && sh /tmp/netdata-kickstart.sh

or

curl https://get.netdata.cloud/kickstart.sh > /tmp/netdata-kickstart.sh && sh /tmp/netdata-kickstart.sh

sudo nano /etc/netdata/stream.conf

[stream]
    enabled = yes
    destination = parent_vm_ip:19999
    api key = 76afe428-665e-4418-b84c-cbb0c374233d

sudo nano /etc/netdata/netdata.conf

sudo chown USERNAME /etc/netdata/

sudo systemctl enable netdata

sudo systemctl restart netdata

# Tiger VNC

sudo apt update -y

sudo apt upgrade -y

sudo apt install tigervnc-standalone-server -y

vncpasswd

nano ~/.vnc/xstartup

#!/bin/sh
unset SESSION_MANAGER
unset DBUS_SESSION_BUS_ADDRESS

/usr/bin/gnome-session

[ -x /etc/vnc/xstartup ] && exec /etc/vnc/xstartup
[ -r $HOME/.Xresources ] && xrdb $HOME/.Xresources
x-window-manager &

chmod +x ~/.vnc/xstartup

<!-- sudo nano /etc/tigervnc/vncserver-config-defaults -->

<!-- vncserver -localhost no -->

sudo nano /etc/systemd/system/vncserver@.service
sudo nano /etc/systemd/system/vncserver@:1.service

sudo systemctl daemon-reload
sudo systemctl enable vncserver@:1.service
sudo systemctl start vncserver@:1.service
sudo systemctl status vncserver@:1.service

# XRDP

sudo apt update -y

sudo apt upgrade -y

sudo apt install xfce4 xfce4-goodies -y

sudo apt install xrdp -y

sudo systemctl status xrdp

sudo systemctl start xrdp

sudo nano /etc/xrdp/xrdp.ini

sudo systemctl restart xrdp

# References

https://raspberrytips.com/tigervnc-server-on-ubuntu/
https://www.digitalocean.com/community/tutorials/how-to-enable-remote-desktop-protocol-using-xrdp-on-ubuntu-22-04
https://phoenixnap.com/kb/xrdp-ubuntu#ftoc-heading-3