# qemu agent
sudo apt update -y

sudo apt upgrade -y

sudo apt install qemu-guest-agent

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
    api key = API_KEY

sudo nano /etc/netdata/netdata.conf

[global]
    hostname = HOST_NAME

sudo systemctl enable netdata

sudo systemctl restart netdata