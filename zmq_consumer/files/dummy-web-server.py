#!/usr/bin/env python

import zmq
import sys
import MySQLdb
import os
import time


mysql_conn = None
while not mysql_conn:
  try:
    mysql_conn = MySQLdb.connect(host= "reto1db",
        user="root",
        passwd="passwd",
        db="reto1")
  except:
    print("Waiting for the DB to start")
    time.sleep(5)


context = zmq.Context()
server = context.socket(zmq.SUB)
server_addr = os.getenv('SERVER_PORT_5556_TCP', 'tcp://SERVER_IP:5556')
if not server_addr:
  print "Unable to attach to server: address not found in SERVER_PORT_5556_TCP"
  sys.exit(-1)

server.connect(server_addr)
topicfilter = 999
server.setsockopt(zmq.SUBSCRIBE, str(topicfilter))
print("Loaded consumer for topic: '%s' on server %s" % (topicfilter, server_addr))

while True:
    topic, messagedata = server.recv_multipart()
    x = mysql_conn.cursor()
    x.execute("""INSERT INTO reto1 VALUES (%s, now())""", messagedata)
    mysql_conn.commit()
    request.send("ok")

server.close()
context.term()
