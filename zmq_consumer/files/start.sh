#!/bin/sh

if [ ! -z ${THEDB+x} ]; then sed -i.bak s/reto1db/$THEDB/ /root/dummy-web-server.py ; fi

# I hate this
export SERVER_IP=$(ping -c1 server | grep -o "(.*)" | tr -d '(' | tr -d ')')
sed -i.bak -e "s/SERVER_IP/$SERVER_IP/" /root/dummy-web-server.py 

python /root/dummy-web-server.py
