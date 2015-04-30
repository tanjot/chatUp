#!/usr/bin/python3
import socket
import sys
import threading
import time
import argparse
import ipaddress

def sendThread(conn, username):
    ''' Provides functionality for sending messages to all peer connected
        '''

    print("Start sending thread....")
    inputStr = input()

    global areSendReceiveWorking
    while inputStr.lower() != "bye" and areSendReceiveWorking:
        msg = username + ": " + inputStr + "\n"
        conn.send( msg.encode() )
        inputStr = input()

    msg = username + ": " + inputStr + "\n"
    conn.send( msg.encode() )

    print("Exit sending thread....")
    areSendReceiveWorking = False

def recvThread(conn, username):
    ''' Provides functionality for receiving message through peer connection
        '''

    print("Start receving thread....")

    global areSendReceiveWorking
    buffSize = 10
    checkOnString = ""
    storedData = ""

    while  checkOnString != "bye" and areSendReceiveWorking:
        try:
            data_recv = str(conn.recv(buffSize).decode())
        #TODO: Find exception name
        except:
            print("Problem in receiving from " + username)
            checkOnString = "bye"
        else:
            for ch in data_recv:
                if ch == '\n':
                    lastPrinted = storedData
                    print( lastPrinted )
                    index = lastPrinted.find(':')
                    checkOnString = lastPrinted[(index+1):].strip()
                    storedData = ""
                else:
                    storedData = storedData + ch

    print("Exit receving thread....")
    areSendReceiveWorking = False

def connectToPeer():
    '''Connects to peer whose address is provided
        '''
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    addr = socket.gethostname()

    global argHandle
    if argHandle.localUsername:
        username = argHandle.localUsername
    else:
        username = "NOname"

    try:
        sock.connect((argHandle.RemoteIPAndPort[0],int(argHandle.RemoteIPAndPort[1])) )
    except ConnectionRefusedError:
        print("Problem in establishing connection using ip : " +
                argHandle.RemoteIPAndPort[0] + " and port: " +
                argHandle.RemoteIPAndPort[1])

    else:
        global areSendReceiveWorking
        areSendReceiveWorking = True

        receivingThread = threading.Thread(target = recvThread, args = (sock,
            username))
        sendingThread = threading.Thread(target = sendThread, args = (sock,
            username ))

        receivingThread.start()
        sendingThread.start()
        receivingThread.join()
        sendingThread.join()
    #if one of the threads dies close the other thread and then the connection
    sock.close()



def validatIP():
    ''' Validates IP address
        '''

    global argHandle
    try:
        ipaddress.ip_address(argHandle.RemoteIPAndPort[0])
    except ValueError:
        print("Remote IP not valid")
        return False
    return True

def handleArguments():
    ''' Adds arguments and and validates them
        '''

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
        print("ip: "+argHandle.RemoteIPAndPort[0], "port: "+
                argHandle.RemoteIPAndPort[1])
        return validatIP()
    return False


def main( arg = sys.argv ):
    if handleArguments():
        global argHandle
        if argHandle:
            connectToPeer()

if __name__ == '__main__':
    main()


