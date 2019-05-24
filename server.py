#!/usr/bin/python

#Jonathan Wein
#jmw34
#002

import sys, time, os.path, struct
from socket import *
from urllib.request import urlopen

argv = sys.argv
serverIP = argv[1]
serverPort = int(argv[2])
dataLen = 10000
serverSocket = socket(AF_INET, SOCK_STREAM)
serverSocket.bind((serverIP, serverPort))

while True:
    serverSocket.listen(1)
    d, address = serverSocket.accept()
    data = d.recv(dataLen)
    format_t = str(len(data)) + "s"
    i = struct.unpack(format_t, data)
    header = i[0].decode('utf-8')

    if not "If-Modified-Since" in header:
        modified = 0
        data = i[0].decode('utf-8')
        i = data.split()
        file = i[1][1:]

    else:
        modified = 1
        data = i[0].decode('utf-8').split("If-Modified-Since: ")
        i = data[0].split()
        modified_date = str(data[1])
        file = i[1][1:]

    if not os.path.exists(file):
        status = i[2] + " 404 Not Found" + "\r\n"
        header = "Date: " + str(time.strftime("%c")) + "\r\n"
        m = status + header

    else:
        f = open(file, "r")
        last_modified = str(time.ctime(os.path.getmtime(file)))

        if ((modified) and (str(modified_date) > str(last_modified))):
            status = i[2] + " 304 Not Modified" + "\r\n"
            header = "Date: " + str(time.strftime("%c")) + "\r\n\r\n"
            m = status + header

        else:
            status = i[2] + " 200 OK" + "\r\n"
            header = "Date: " + str(time.strftime("%c")) + "\r\n"
            header += "Last-Modified: " + last_modified + "\r\n"
            header += "Content-Length: " + str(os.path.getsize(file)) + "\r\n\r\n"
            content = f.read()
            m = status + header + content

    m = m.encode('utf-8')
    format_t = str(len(m) + 1) + "s"
    msg = struct.pack(format_t, m)
    d.send(msg)
    d.close()
serverSocket.close()
