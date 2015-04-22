#!/usr/bin/python3
import socket
import sys
import threading
import time

def sendThread(conn, username):
    print("send:")
    #time.sleep(5)
    #print("Recv end ")
    inputStr = input(username + ": ")#+username + ': ')

    while inputStr.lower() != "bye":
        msg = username + ": " + inputStr + "\n"
        #print(msg)
        #conn.send( str(len(msg)).encode() )
        conn.send( msg.encode()  )
        inputStr = input(username + ": ")
    conn.send( str(len(msg)).encode() )


    conn.close()

def recvThread(conn, username):
    print("REcV")
    #time.sleep(5)
    #print("Recv end ")

    buffSize = 10
    lastPrinted = ""
    storedData = ""
    while  lastPrinted != "bye":
        data_recv = str(conn.recv(buffSize).decode())

        for ch in data_recv:
            if ch == '\n':
                print("Msg: " + storedData)
                lastPrinted = storedData
                print( lastPrinted )
                storedData = ""
            else:
                storedData = storedData + ch
    print("Msg: " + storedData)
    sock.close()



def connectToPeer(peerPort):

    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    addr = socket.gethostname()

    sock.connect( (addr, peerPort) )
    receivingThread = threading.Thread(target = recvThread, args = (sock, str(addr)))
    sendingThread = threading.Thread(target = sendThread, args = (sock, str(addr) ))

    receivingThread.start()
    sendingThread.start()
    ##join and close socket
#sock.close()


def main( arg = sys.argv ):
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    print('In setUpLocalConnection port: '+(arg[1]))
    localAddr = socket.gethostname()
    port = int(arg[1])

    sock.bind( (localAddr, port) )
    sock.listen(1)


    connectToPeer(int(arg[2]))
#sock.close()

if __name__ == '__main__':
    main()


