#!/usr/bin/python3
import socket

def connectionFun():
    print('In conn fun')
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    myAddr = socket.gethostname()
    port = 8888

    sock.bind((myAddr, port))

    sock.listen(5)

    while True:
        conn, peerAddr = sock.accept()
        print(' Accepted request from addr: ' , peerAddr)
        msg = "Hie we are connected how are you bye "
        conn.send(msg.encode())
        conn.close()


def main():
    print('In main')
    connectionFun()

if __name__ == '__main__':
    print(' in name')
    main()



