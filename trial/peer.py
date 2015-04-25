#!/usr/bin/python3
import socket
import sys
import threading
import time

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

def connectToPeer(localPort, peerPort):

    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    addr = socket.gethostname()

    #sock.bind( (addr, localPort) )

    sock.connect( (addr, peerPort) )
    receivingThread = threading.Thread(target = recvThread, args = (sock, str(addr)))
    sendingThread = threading.Thread(target = sendThread, args = (sock, str(addr) ))

    receivingThread.start()
    sendingThread.start()
    receivingThread.join()
    sendingThread.join()
    sock.close()


def main( arg = sys.argv ):
    #sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    #print('In setUpLocalConnection port: '+(arg[1]))
    #localAddr = socket.gethostname()
    #port = int(arg[1])

    #sock.bind( (localAddr, port) )
    #sock.listen(1)


    connectToPeer(int(arg[1]), int(arg[2]))
#sock.close()

if __name__ == '__main__':
    main()


