#!/usr/bin/python3
import socket

def connectionClientFun():
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    #localhost bcoz communication is local
    addr = socket.gethostname()
    port = 8888

    sock.connect((addr, port))

    buffSize = 10
    lastPrinted = ""
    storedData = ""
    while  lastPrinted != "bye":
        data_recv = str(sock.recv(buffSize).decode())

        for ch in data_recv:
            if ch == ' ':
                print("Msg: " + storedData)
                lastPrinted = storedData
                print(" last Msg: " + lastPrinted)
                storedData = ""
            else:
                storedData = storedData + ch
    print("Msg: " + storedData)
    sock.close()
    #count = 0
    #bytesRead = sock.recv(10)
    #while bytesRead != ' ':
    #    print('Message received: ' + str(bytesRead.decode()) )
    #    bytesRead = sock.recv(10)
    #    count += 1
    #print('Message received: ' + str(sock.recv(10).decode()) )

def main():
    connectionClientFun()

if __name__ == '__main__':
    main()



