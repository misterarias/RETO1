#!/usr/bin/env python

# Taken from. http://zguide.zeromq.org/py:asyncsrv (sharing is caring)
import zmq
import sys
import MySQLdb

context = zmq.Context(1)
server = context.socket(zmq.REP)
server.bind("tcp://*:5570")

mysql_conn = MySQLdb.connect(host= "reto1db",
                  user="root",
                  passwd="passwd",
                  db="reto1")
print("Loaded consumer")
while True:
    request = server.recv()
    x = mysql_conn.cursor()
    x.execute("""INSERT INTO reto1 VALUES (%s, now())""", request)
    mysql_conn.commit()
    request.send("ok")

server.close()
context.term()
