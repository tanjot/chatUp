#!usr/bin/python3
import socket
import sys

def acceptPeerConn(sock):
    print('In acceptPeerConnections')

    while True:
        peerConn, peerAddr = sock.accept()
        #start thread for each peer and handle both sending and receiving
        peerConn.send( "hi we are connected".encode() )
        print("hi: "+str(peerConn.recv(1024).decode()))
        peerConn.close()

def connectToPeer(peerPort):

    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    addr = socket.gethostname()
    
    sock.connect( (addr, peerPort) )
    print("Hi:  "+str(sock.recv(1024).decode()) )
    sock.send('coneected: '.encode())
    sock.close()


def main( arg = sys.argv ):
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    print('In setUpLocalConnection')
    localAddr = socket.gethostname()
    port = int(arg[1]) 
                                                             
    sock.bind( (localAddr, port) )
    sock.listen(5) 


    if len(arg) > 2 :
        for i in arg:
            print('Connecting to peer'+i)
        connectToPeer( int(arg[2]) ) 
    else:
        acceptPeerConn(sock)  

    sock.close()

if __name__ == '__main__':
    main()



