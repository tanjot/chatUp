#!/usr/bin/python3
import socket
import sys
import threading
import time
import argparse
import ipaddress

def sendThread(conn, username):
    print("Sending thread started....")
    inputStr = input()

    while inputStr.lower() != "bye":
        msg = username + ": " + inputStr + "\n"
        conn.send( msg.encode()  )
        inputStr = input()
    msg = username + ": " + inputStr + "\n"
    conn.send( msg.encode() )

    print("Sending thread started....")
    #conn.close()

def recvThread(conn, username):
    print("Receving thread started....")

    buffSize = 10
    checkOnString = ""
    storedData = ""
    while  checkOnString != "bye":
        data_recv = str(conn.recv(buffSize).decode())

        for ch in data_recv:
            if ch == '\n':
                lastPrinted = storedData
                print( lastPrinted )
                index = lastPrinted.find(':')
                checkOnString = lastPrinted[(index+1):].strip()
                storedData = ""
            else:
                storedData = storedData + ch

    print("Receving thread ended....")

def connectToPeer():

    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    addr = socket.gethostname()

    #sock.bind( (addr, localPort) )
    global argHandle
    if argHandle.localUsername:
        username = argHandle.localUsername
    else:
        username = "NOname"

    sock.connect((argHandle.RemoteIPAndPort[0],int(argHandle.RemoteIPAndPort[1])) )
    receivingThread = threading.Thread(target = recvThread, args = (sock,
        username))
    sendingThread = threading.Thread(target = sendThread, args = (sock,
        username ))

    receivingThread.start()
    sendingThread.start()
    receivingThread.join()
    sendingThread.join()
    sock.close()



def validatIP():
    global argHandle
    try:
        ipaddress.ip_address(argHandle.RemoteIPAndPort[0])
    except:
        print("Remote IP not valid")
        return False
    return True

def handleArguments():
    parser = argparse.ArgumentParser()
   # parser.add_argument("localPort", help= "Local port number to bind with",
   #         type = int)
    parser.add_argument("--localUsername", "-u", help = "Username to be"
        "assigned")
    parser.add_argument("RemoteIPAndPort",type = str, nargs = 2, help = "IP address and port"
        "number of the remote connection")


    global argHandle
    argHandle = parser.parse_args()
    if argHandle.RemoteIPAndPort:
        return validatIP()
        print("ip: "+argHandle.RemoteIPAndPort[0], "port: "+
                argHandle.RemoteIPAndPort[1])
    return False


def main( arg = sys.argv ):
    if handleArguments():
        global argHandle
        if argHandle:
            connectToPeer()
#TODO: Close socket properly

if __name__ == '__main__':
    main()


