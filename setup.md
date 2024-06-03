# Github Repository

git clone https://github.com/LMY03/CAP2240_API.git

docker compose -f ~/CAP2240_API/docker-compose.yml up --build -d

### FOR UPDATES ONLY

df -h

du -ah / | sort -rh | head -n 20

sudo apt-get clean

sudo apt-get autoremove

sudo rm -rf /tmp/*

docker system prune -a -y

sudo find /var/log -type f -delete

git -C CAP2240_API pull origin main

docker compose -f ~/CAP2240_API/docker-compose.yml up --build -d

### FOR UPDATES ONLY

# GUACAMOLE

mkdir -p ~/guacamole-initdb

docker run --rm guacamole/guacamole /opt/guacamole/bin/initdb.sh --mysql > ~/guacamole-initdb/initdb.sql

docker cp ~/guacamole-initdb/initdb.sql mysql:/docker-entrypoint-initdb.d

docker exec -it mysql bash


cd /docker-entrypoint-initdb.d

mysql -u root -p


CREATE DATABASE IF NOT EXISTS guacamole_db;

CREATE USER IF NOT EXISTS 'guacadmin'@'%' IDENTIFIED BY 'guacpassword';

GRANT SELECT, UPDATE, INSERT, DELETE ON guacamole_db.* TO 'guacadmin'@'%';

flush privileges;

use guacamole_db;

source initdb.sql;

exit;

exit

# NETDATA

# generate API_KEY
uuidgen

# Login as root in docker container
docker exec -it netdata /bin/bash

vi /etc/netdata/stream.conf

# plugin API_KEY 
[API_KEY] 
    enabled = yes

# logout of docker container
exit

exit

docker restart netdata

# ANSIBLE

docker exec -it ansible /bin/sh

vi ../inventory/hosts

IP_ADDRESS_OF_NODE_VM ansible_user=USER_NAME

ssh-copy-id USER_NAME@IP_ADDRESS_OF_NODE_VM

docker exec -it ansible ansible all -i /inventory/hosts -m ping

rm -rf ~/.ssh

# References

https://www.youtube.com/watch?v=sYNfPqAN3H4&t
https://learn.netdata.cloud/docs/netdata-agent/installation/docker#create-a-new-netdata-agent-container

# Containerize
https://www.youtube.com/watch?v=GGb1C-4mTCw