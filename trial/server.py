#!/usr/bin/python3
import socket
import sys
import threading
import argparse
import ipaddress

def sendThread(conn, username):
    print("Sending thread started....")

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

    print("Sending thread ended....")
    isSendThreadWorking = False

def removeConnFromList(conn = None):
    global peerList
    if conn is None:
        for it in peerList:
            peerList.remove(it)
            it.close()
    else:
        peerList.remove(conn)
        conn.close()

def recvThread(conn, username):
    print("Receving thread started....")

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
    print("Receving thread ended....")


def startConnectionThreads(peerConn):
    global argHandle
    global peerList

    if argHandle.localUsername:
        username = argHandle.localUsername
    else:
        username = "NOname"

    receivingThread = threading.Thread(target = recvThread, args = (peerConn,
        username))
    receivingThread.start()
   # if len(peerList) == 0:
   #     sendingThread = threading.Thread(target = sendThread, args = (peerConn,
   #     username))
   #     sendingThread.start()
   #     receivingThread.start()
   #     sendingThread.join()
   #     receivingThread.join()
   # else:
   #     receivingThread.start()
   #     receivingThread.join()
    receivingThread.join()
    #peerList.remove(peerConn)
    #peerConn.close()


def acceptPeerConn(sock):
    print('In acceptPeerConnections')

    global peerList
    peerList = []

    global isSendThreadWorking

    sendingThread = threading.Thread(target = sendThread, args = (sock,
    "Server"))
    sendingThread.start()
    isSendThreadWorking = True

    while isSendThreadWorking:
        print("in while loop")
        peerConn, peerAddr = sock.accept()

        peerList.append(peerConn)
        acceptPeerConnThread = threading.Thread(target = startConnectionThreads, args =
                (peerConn,) )
        acceptPeerConnThread.start()

       # if argHandle.localUsername:
       #     username = argHandle.localUsername
       # else:
       #     username = "NOname"

       # receivingThread = threading.Thread(target = recvThread, args = (peerConn,
       #     username))
       # receivingThread.start()
    print("Out of Loop")
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

    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    print('In setUpLocalConnection port: '+str(argHandle.localPort))
    localAddr = socket.gethostname()
    port = int(argHandle.localPort)

    sock.bind( (localAddr, port) )
    sock.listen(2)

    #TODO: close socket appropriately

    acceptPeerConnThread = threading.Thread(target = acceptPeerConn, args =
            (sock,) )
    acceptPeerConnThread.start()
    acceptPeerConnThread.join()

    if handleArguments():
        #create connection to that remote
        print("No functionality for connecting to Peer")
    print("End of main...")


if __name__ == '__main__':
    main()

