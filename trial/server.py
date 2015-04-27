#!/usr/bin/python3
import socket
import sys
import threading
import argparse
import ipaddress


def removeConnFromList(conn = None):
    ''' Removes and closes all peer connection from list if no connection is
        provided else removes the particular connection provided in argument
        '''
    global peerList
    if conn is None:
        for it in peerList:
            peerList.remove(it)
            it.close()
    else:
        peerList.remove(conn)
        conn.close()

def sendThread(sock, username):
    ''' Provides functionality for sending messages to all peer connected
        '''
    print("Start sending thread....")

    global peerList
    global isSendThreadWorking

    inputStr = input()
    while inputStr.lower() != "bye":
        msg = username + ": " + inputStr + "\n"
        for conn in peerList:
            conn.send( msg.encode()  )

        inputStr = input()

    msg = username + ": " + inputStr + "\n"
    for conn in peerList:
        conn.send( msg.encode() )

    print("Exit sending thread....")
    isSendThreadWorking = False

def recvThread(conn, username):
    ''' Provides functionality for receiving message through peer connection
        '''
    print("Starting receving thread....")

    global isSendThreadWorking

    buffSize = 10
    checkOnString = ""
    storedData = ""
    while checkOnString != "bye" and isSendThreadWorking:
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
    if isSendThreadWorking:
        removeConnFromList(conn)
    else:
        removeConnFromList()
    print("Exit receiving thread....")


def acceptPeerConn(sock):
    ''' Accepts a connection request and starts a separate receiving thread for
        each connection
        '''

    global peerList
    peerList = []

    global isSendThreadWorking
    global argHandle

    if argHandle.localUsername:
        username = argHandle.localUsername
    else:
        username = "Server"

    #accepts connection until send thread does not end the connection
    while isSendThreadWorking:

        print("Waiting for peer connection")
        peerConn, peerAddr = sock.accept()

        peerList.append(peerConn)

        receivingThread = threading.Thread(target = recvThread, args = (peerConn,
            username))
        receivingThread.start()


def validatIP():
    ''' Validates IP address
        '''
    global argHandle

    try:
        ipaddress.ip_address(argHandle.RemoteIPAndPort[0])
    except:
        print("Remote IP not valid")
        return False
    return True

def handleArguments():
    ''' Adds arguments and and validates them
        '''
    parser = argparse.ArgumentParser()
    parser.add_argument("localPort", help= "Local port number to bind with",
            type = int)
    parser.add_argument("--localUsername", "-u", help = "Username to be"
        "assigned")
    parser.add_argument("--RemoteIPAndPort", "-r",type = str, nargs = 2, help = "IP address and port"
        "number of the remote connection")


    global argHandle
    argHandle = parser.parse_args()
    if argHandle.RemoteIPAndPort:
        return validatIP()
        print("ip: "+argHandle.RemoteIPAndPort[0], "port: "+
                argHandle.RemoteIPAndPort[1])
    #Bcoz Remoteipandport is optional
    return True

def main( arg = sys.argv ):

    handleArguments()
    global argHandle

    #Creating socket
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    localAddr = socket.gethostname()
    port = int(argHandle.localPort)

    #Binding address with socket
    sock.bind( (localAddr, port) )
    sock.listen(2)

    if argHandle.localUsername:
        username = argHandle.localUsername
    else:
        username = "Server"

    #Creating threads
    sendingThread = threading.Thread(target = sendThread, args = (sock,
    username))
    acceptPeerConnThread = threading.Thread(target = acceptPeerConn, args =
            (sock,) )
    acceptPeerConnThread.setDaemon(True)

    global isSendThreadWorking

    sendingThread.start()
    isSendThreadWorking = True
    acceptPeerConnThread.start()
    sendingThread.join()
    sock.close()

   # if handleArguments():
   #     #create connection to that remote
   #     print("No functionality for connecting to Peer")
    print("End of main...")


if __name__ == '__main__':
    main()

