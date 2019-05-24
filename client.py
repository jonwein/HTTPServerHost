#!/usr/bin/python

#Jonathan Wein
#jmw34
#002

import os, sys, time
from socket import *
import struct, json
from pprint import pprint

if ':' not in sys.argv[1]:
    gethostport = sys.argv[1].split('/')
    host = gethostport[0]
    port = 80
    file = gethostport[1]

else:
    gethostport = sys.argv[1].split(':')
    host = gethostport[0]
    port = int(gethostport[1].split('/')[0])
    file = gethostport[1].split('/')[1]

count = 10000

clientsocket = socket(AF_INET, SOCK_STREAM)
send = (host, port)
clientsocket.connect(send)

get = "GET /" + file + " HTTP/1.1 " + "\r\n" + "Host: " + host + ":" + str(port) + "\r\n"

if not (os.path.exists('cache.txt')):
    cf = open('cache.txt','w+')
    cf.close()

f = open('cache.txt', 'r')
lines = f.readlines()
f.close()

for line in lines:
    if file in line:
        date = line.split("If-Modified-Since")[1].split("'")[2]
        get += "If-Modified-Since: " + str(date) + "\r\n"
        break
get += "\r\n"

format_t = str(len(get) + 1) + "s"
get = get.encode('utf-8')
m = struct.pack(format_t, get)
clientsocket.sendall(m)
data_echo = clientsocket.recv(count)
format_t = str(len(data_echo)) + "s"
i = struct.unpack(format_t, data_echo)
data = i[0].decode('utf-8')
data = data.split("\r\n\r\n")
head = data[0].split("\n")
status = head[0]
code = int(status.split()[1])

if code is 200:
    content = data[1]
    contents = "Contents: " + "\n" + str(content)
    last_modified = head[2].split("Last-Modified: ")[1].strip('\r')

elif code == 304:
    receive = "304 Not Modified"

else:
    receive = "404 Not Found"

if (code == 304 or code == 404):
    print(receive)

elif code == 200:
    print(content)

    w = open('cache1.txt', 'w')
    for line in lines:
        if file not in line:
            w.write(line + '\n')

    cache_line = {'url': file, 'If-Modified-Since': last_modified, 'content': content}
    w.write(str(cache_line))
    w.close()
    os.remove('cache.txt')
    os.rename('cache1.txt', 'cache.txt')

clientsocket.close()
