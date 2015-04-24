#!/usr/bin/python3
import socket
import sys
import threading

def sendThread(conn, username):
    print("Sending thread started....")
    inputStr = input()#+username + ': ')

    while inputStr.lower() != "bye":
        msg = username + ": " + inputStr + "\n"
        #print("local: "+msg)
        #conn.send( str(len(msg)).encode() )
        conn.send( msg.encode()  )
        inputStr = input()
    msg = username + ": " + inputStr + "\n"
    print("end end end "+msg)
    conn.send( msg.encode() )

    #conn.close()

def recvThread(conn, username):
    print("Receving thread started....")

    buffSize = 10
    lastPrinted = ""
    storedData = ""
    while  lastPrinted != "bye":
        data_recv = str(conn.recv(buffSize).decode())

        for ch in data_recv:
            if ch == '\n':
                lastPrinted = storedData
                print( lastPrinted )
                storedData = ""
            else:
                storedData = storedData + ch
    #print("Msg: " + storedData)
    #sock.close()


def acceptPeerConn(sock):
    print('In acceptPeerConnections')

    #while True:
    peerConn, peerAddr = sock.accept()
    receivingThread = threading.Thread(target = recvThread, args = (peerConn,
    "Tanjot"))
    sendingThread = threading.Thread(target = sendThread, args = (peerConn,
        "Tanjot" ))
    #start thread for each peer and handle both sending and receiving
                                                                              #thread = threading.Thread(target = sendThread, args = (peerConn, "Tanjot"))
    receivingThread.start()                                                          #thread.start()
    sendingThread.start()                                                                #recvThread(peerConn, str(peerAddr))
    #peerConn.close()


def main( arg = sys.argv ):
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    print('In setUpLocalConnection port: '+(arg[1]))
    localAddr = socket.gethostname()
    port = int(arg[1])

    sock.bind( (localAddr, port) )
    sock.listen(1)
    acceptPeerConn(sock)

#sock.close()

if __name__ == '__main__':
    main()

