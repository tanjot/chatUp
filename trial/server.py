#!/usr/bin/python3
import socket
import sys
import threading

def sendThread(conn, username):
    print("Sending thread started....")
    inputStr = input()

    while inputStr.lower() != "bye":
        msg = username + ": " + inputStr + "\n"
        conn.send( msg.encode()  )
        inputStr = input()
    msg = username + ": " + inputStr + "\n"
    conn.send( msg.encode() )
    print("Sending thread ended....")

def recvThread(conn, username):
    print("Receving thread started....")

    buffSize = 10
    checkOnString = ""
    storedData = ""
    while checkOnString != "bye":
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


def startConnectionThreads(peerConn):
    receivingThread = threading.Thread(target = recvThread, args = (peerConn,
    "Tanjot"))
    sendingThread = threading.Thread(target = sendThread, args = (peerConn,
    "Tanjot" ))
    sendingThread.start()
    receivingThread.start()
    receivingThread.join()
    sendingThread.join()
    print("join ended")
    peerConn.close()


def acceptPeerConn(sock):
    print('In acceptPeerConnections')

    while True:
        print("in while loop")
        peerConn, peerAddr = sock.accept()
        #acceptPeerConn(sock)
        acceptPeerConnThread = threading.Thread(target = startConnectionThreads, args =
                (peerConn,) )
        acceptPeerConnThread.start()

def main( arg = sys.argv ):
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    print('In setUpLocalConnection port: '+(arg[1]))
    localAddr = socket.gethostname()
    port = int(arg[1])

    sock.bind( (localAddr, port) )
    sock.listen(2)

    #noOfConnections = 0
    #while noOfConnections<2:
    #    acceptPeerConnThread = threading.Thread(target = acceptPeerConn, args =
    #        (sock) )
    #    acceptPeerConnThread.start()
    #    noOfConnections += 1
    #TODO: close socket appropriately


    acceptPeerConnThread = threading.Thread(target = acceptPeerConn, args =
            (sock,) )
    acceptPeerConnThread.start()
    acceptPeerConnThread.join()

    print("End of main...")

#sock.close()

if __name__ == '__main__':
    main()

